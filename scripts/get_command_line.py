#!/usr/bin/env python3

# Copyright 2021 Lucille Delisle
import sys
import argparse
from bioblend.galaxy import GalaxyInstance


def update_tables(gi, dataset_id, replacement_table={}, visited_dataset_ids=[], command_lines_rev_order=[]):
    if dataset_id not in visited_dataset_ids:
        print(f"Visiting {dataset_id}")
        dataset_info = gi.datasets.show_dataset(dataset_id)
        file_name = dataset_info['name'] + '.' + dataset_info['file_ext']
        try:
            file_path = dataset_info['file_name']
            if file_path != '':
                replacement_table[file_path] = file_name
        except Exception:
            pass
        job_info = gi.jobs.show_job(dataset_info['creating_job'])
        if job_info['tool_id'] != 'upload1':
            outputs_ids = [o['id'] for o in job_info['outputs'].values() if o['id'] != dataset_id]
            for oid in outputs_ids:
                output_info = gi.datasets.show_dataset(oid)
                output_file_name = output_info['name'] + '.' + output_info['file_ext']
                try:
                    output_file_path = output_info['file_name']
                    if output_file_path != '':
                        replacement_table[output_file_path] = output_file_name
                except Exception:
                    pass
            prefix = '# ' + job_info['tool_id'] + '\n# command_version:' + job_info['command_version'] + '\n'
            command_lines_rev_order.append(prefix + job_info['command_line'])
            visited_dataset_ids.append(dataset_id)
            inputs_ids = [o['id'] for o in job_info['inputs'].values()]
            for iid in inputs_ids:
                replacement_table, visited_dataset_ids, command_lines_rev_order = update_tables(gi, iid, replacement_table, visited_dataset_ids, command_lines_rev_order)
        else:
            visited_dataset_ids.append(dataset_id)
    return [replacement_table, visited_dataset_ids, command_lines_rev_order]


def replace_all(command_lines, replacement_table):
    for key, value in replacement_table.items():
        command_lines = command_lines.replace(key, value)
    return command_lines


def parse_arguments(args=None):
    argp = argparse.ArgumentParser(
        description=("Write all commandlines used to generate a dataset from a dataset id."))
    argp.add_argument('--url', default='galaxyduboule.epfl.ch',
                      help="A FQDN or IP for a given instance of Galaxy.")
    argp.add_argument('--api', default=None, required=True,
                      help="Your API key. Can be obtained from the webpage."
                      " User - Settings - Manage API key")
    argp.add_argument('--datasetID', default=None, required=True,
                      help="Dataset id")
    return(argp)


def main(args=None):
    args = parse_arguments().parse_args(args)
    gi = GalaxyInstance(args.url, key=args.api)
    replacement_table, visited_dataset_ids, \
        command_lines_rev_order = update_tables(gi, args.datasetID)

    command_lines = []
    # Remove duplicates:
    [command_lines.append(item) for item in command_lines_rev_order[::-1] if item not in command_lines]

    command_lines_with_names = replace_all('\n\n'.join(command_lines), replacement_table)

    command_lines_with_names_noesp = command_lines_with_names.replace('&&', '\n')
    print("\n\nCommand-lines:\n\n")
    print(command_lines_with_names_noesp)


if __name__ == "__main__":
    args = None
    if len(sys.argv) == 1:
        args = ["--help"]
    main(args)
