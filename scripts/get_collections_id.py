#!/usr/bin/env python3

# Copyright 2021 Lucille Delisle
import sys
import argparse
from bioblend.galaxy import GalaxyInstance


# From rhoitjadhav on https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return size


def write_collections(gi, histories_id, fo):
    fo.write("collection_id\thistory_id\thid\tcollection_name\tnb_datasets\thistory_name\n")
    for history_id in histories_id:
        history_name = gi.histories.show_history(history_id)['name']
        collection_ids = [c['id'] for c in gi.histories.show_history(history_id, contents=True, types='dataset_collection')]
        sys.stderr.write(f"Found {len(collection_ids)} in {history_name}.\n")
        for collection_id in collection_ids:
            try:
                full_size = sum([e['object']['file_size']
                                 for e in gi.histories.show_dataset_collection(history_id, collection_id)['elements']])
            except KeyError:
                full_size = sum([ee['object']['file_size']
                                 for e in gi.histories.show_dataset_collection(history_id, collection_id)['elements']
                                 for ee in e['object']['elements']])
            fo.write(f"{collection_id}\t{history_id}"
                     f"\t{gi.histories.show_dataset_collection(history_id, collection_id)['hid']}"
                     f"\t{gi.histories.show_dataset_collection(history_id, collection_id)['name']}"
                     f"\t{convert_bytes(full_size)}"
                     f"\t{history_name}\n")


def getHistories(gi, historiesTable, deleted):
    sys.stderr.write("Getting list of all histories...")
    all_histories = [h['id'] for h in gi.histories.get_histories(deleted=deleted)]
    sys.stderr.write("Done.\n")
    sys.stderr.write(f"Found {len(all_histories)} histories.\n")
    if historiesTable is None:
        return(all_histories)
    else:
        histories = []
        with open(historiesTable, 'r') as f:
            for i, line in enumerate(f, 1):
                potential_hist = line.split()[0]
                if potential_hist in all_histories:
                    histories.append(potential_hist)
                else:
                    sys.stderr.write(f"The history id line {i} ({potential_hist}) is not part of histories. Will be ignored.\n")
        sys.stderr.write(f"Will process {len(histories)} histories.\n")
        return(histories)


def parse_arguments(args=None):
    argp = argparse.ArgumentParser(
        description=("Get all collections ids from history ids."))
    argp.add_argument('--url', default='galaxyduboule.epfl.ch',
                      help="A FQDN or IP for a given instance of Galaxy.")
    argp.add_argument('--api', default=None, required=True,
                      help="Your API key. Can be obtained from the webpage."
                      " User - Settings - Manage API key")
    argp.add_argument('--historiesTable', default=None,
                      help="[Optional] Input table with one line per history."
                      " It should correspond to the History API ID.")
    argp.add_argument('--deleted', default=False, action='store_true',
                      help="Get the deleted histories only.")
    argp.add_argument('--output', default=sys.stdout,
                      type=argparse.FileType('w'),
                      help="Output table.")
    return(argp)


def main(args=None):
    args = parse_arguments().parse_args(args)
    gi = GalaxyInstance(args.url, key=args.api)
    histories = getHistories(gi, args.historiesTable, args.deleted)
    write_collections(gi, histories, args.output)


if __name__ == "__main__":
    args = None
    if len(sys.argv) == 1:
        args = ["--help"]
    main(args)
