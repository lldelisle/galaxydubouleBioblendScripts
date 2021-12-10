#!/usr/bin/env python3

# Copyright 2021 Lucille Delisle
import os
import sys
import argparse
from bioblend.galaxy import GalaxyInstance


def download_element(gi, e, current_output_folder):
    identifier = e['element_identifier']
    # If simple collection:
    dataset_id = e['object']['id']
    dataset_ext = e['object']['file_ext']
    if not dataset_ext or dataset_ext == 'auto' or dataset_ext == '_sniff_':
        dataset_ext = 'data'
    output_file = os.path.join(current_output_folder, f"{identifier}.{dataset_ext}")
    if e['object']['purged']:
        print(f"Could not download {identifier} because it has been purged.")
    else:
        try:
            gi.datasets.download_dataset(dataset_id,
                                            file_path=output_file,
                                            use_default_filename=False)
        except Exception:
            print("Could not download.")


def download_collections(gi, collection_table, output_folder):
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    with open(collection_table, 'r') as f:
        for i, line in enumerate(f, 1):
            ls = line.split()
            if len(ls) < 2:
                print(f"Skipping line {i}")
                continue
            potential_collection = line.split()[0]
            potential_history = line.split()[1]
            try:
                infos = gi.histories.show_dataset_collection(potential_history, potential_collection)
            except Exception:
                infos = None
            if not isinstance(infos, dict):
                if i != 1 or potential_collection != 'collection_id':
                    print(f"Error line {i}:")
                    print(infos)
                    print("Line ignored.")
            else:
                history_name = gi.histories.show_history(infos['history_id'])['name']
                collection_name = infos['name']
                collection_hid = infos['hid']
                current_output_folder = os.path.join(output_folder,
                                                     infos['history_id'] + "_" + history_name.replace(' ', '_'),
                                                     str(collection_hid) + "_" + collection_name.replace(' ', '_'))
                if not os.path.isdir(current_output_folder):
                    os.makedirs(current_output_folder)
                print(f"Downloading {collection_name} in {current_output_folder}")
                for e in infos['elements']:
                    if e['element_type'] == 'hda':
                        # This was a simple collection
                        print(f"Downloading {e['element_identifier']}")
                        download_element(gi, e, current_output_folder)
                    else:
                        # This was a collection of pairs:
                        new_output_folder = os.path.join(current_output_folder, e['element_identifier'])
                        if not os.path.isdir(new_output_folder):
                            os.makedirs(new_output_folder)
                        for ee in e['object']['elements']:
                            print(f"Downloading {ee['element_identifier']}")
                            download_element(gi, ee, new_output_folder)


def parse_arguments(args=None):
    argp = argparse.ArgumentParser(
        description=("Download collections from collection ids."))
    argp.add_argument('--url', default='galaxyduboule.epfl.ch',
                      help="A FQDN or IP for a given instance of Galaxy.")
    argp.add_argument('--api', default=None, required=True,
                      help="Your API key. Can be obtained from the webpage."
                      " User - Settings - Manage API key")
    argp.add_argument('--collectionTable', default=None, required=True,
                      help="Input table with one line per collection."
                      " It needs to be generated by get_collections.py"
                      " (first column collection id, second column history id).")
    argp.add_argument('--outputFolder', default=None, required=True,
                      help="Folder where files will be downloaded.")
    return(argp)


def main(args=None):
    args = parse_arguments().parse_args(args)
    gi = GalaxyInstance(args.url, key=args.api)
    download_collections(gi, args.collectionTable, args.outputFolder)


if __name__ == "__main__":
    args = None
    if len(sys.argv) == 1:
        args = ["--help"]
    main(args)
