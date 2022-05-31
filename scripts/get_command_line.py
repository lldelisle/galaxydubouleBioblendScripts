#!/usr/bin/env python3

# Copyright 2021 Lucille Delisle
import sys
import argparse
from bioblend.galaxy import GalaxyInstance
import re

default_parameters = {
    "toolshed.g2.bx.psu.edu/repos/lparsons/cutadapt/cutadapt/1.16.8":
    {
        "-j": 1,
        "--cores": 1,
        "-e": 0.1,
        "--error-rate": 0.1,
        "--no-indels": "allow",
        "-n": 1,
        "--times": 1,
        "-O": 3,
        "--overlap": 3,
        "--quality-base": 33,
        "-m": 0,
        "--minimum-length": 0,
        "--pair-filter": "any"
    },
    "toolshed.g2.bx.psu.edu/repos/lparsons/cutadapt/cutadapt/1.16.1":
    {
        "-j": 1,
        "--cores": 1,
        "-e": 0.1,
        "--error-rate": 0.1,
        "--no-indels": "allow",
        "-n": 1,
        "--times": 1,
        "-O": 3,
        "--overlap": 3,
        "--quality-base": 33,
        "-m": 0,
        "--minimum-length": 0,
        "--pair-filter": "any"
    },
    "testtoolshed.g2.bx.psu.edu/repos/lldelisle/cooler/cooler_balance/0.0.1":
    {
        "-p": 8,
        "--nproc": 8,
        "-c": 10000000,
        "--chunksize": 10000000,
        "--mad-max": 5,
        "--min-nnz": 10,
        "--min-count": 0,
        "--ignore-diags": 2,
        "--tol": "1e-05",
        "--max-iters": 200,
        "--name": "weight",
        "--convergence-policy": "store_final"
    },
    "toolshed.g2.bx.psu.edu/repos/iuc/macs2/macs2_callpeak/2.1.1.20160309.3":
    {
        "-f": "AUTO",
        "-g": "hs",
        "--keep-dup": 1,
        "--buffer-size": 100000,
        "--verbose": 2,
        "--bw": 300,
        "-m": [5, 50],
        "--mfold": [5, 50],
        "--shift": 0,
        "--extsize": 200,
        "-q": 0.05,
        "--qvalue": 0.05,
        "--slocal": 1000,
        "--llocal": 10000,
        "--broad-cutoff": 0.1,
        "--fe-cutoff": 1
    },
    "toolshed.g2.bx.psu.edu/repos/iuc/rgrnastar/rna_star/2.7.7a":
    {
        "--runMode": "alignReads",
        "--runThreadN": 1,
        "--runDirPerm": "User_RWX",
        "--runRNGseed": 777,
        "--genomeDir": "./GenomeDir/",
        "--genomeLoad": "NoSharedMemory",
        "--genomeFileSizes": 0,
        "--genomeChrBinNbits": 18,
        "--genomeSAindexNbases": 14,
        "--genomeSAsparseD": 1,
        "--genomeSuffixLengthMax": -1,
        "--genomeType": "Full",
        "--sjdbGTFfeatureExon": "exon",
        "--sjdbGTFtagExonParentTranscript": "transcript_id",
        "--sjdbGTFtagExonParentGene": "gene_id",
        "--sjdbGTFtagExonParentGeneName": "gene_name",
        "--sjdbOverhang": 100,
        "--sjdbScore": 2,
        "--sjdbInsertSave": "Basic",
        "--readFilesType": "Fastx",
        "--readMapNumber": -1,
        "--readMatesLengthsIn": "NotEqual",
        "--readNameSeparator": "/",
        "--readQualityScoreBase": 33,
        "--clip3pNbases": 0,
        "--clip5pNbases": 0,
        "--clip3pAdapterMMp": 0.1,
        "--clip3pAfterAdapterNbases": 0,
        "--limitGenomeGenerateRAM": 31000000000,
        "--limitIObufferSize": 150000000,
        "--limitOutSAMoneReadBytes": 100000,
        "--limitOutSJoneRead": 1000,
        "--limitOutSJcollapsed": 1000000,
        "--limitBAMsortRAM": 0,
        "--limitSjdbInsertNsj": 1000000,
        "--limitNreadsSoft": -1,
        "--outFileNamePrefix": "./",
        "--outStd": "Log",
        "--outQSconversionAdd": 0,
        "--outMultimapperOrder": "Old_2.4",
        "--outSAMtype": "SAM",
        "--outSAMmode": "Full",
        "--outSAMstrandField": "None",
        "--outSAMattributes": "Standard",
        "--outSAMattrIHstart": 1,
        "--outSAMunmapped": "None",
        "--outSAMorder": "Paired",
        "--outSAMprimaryFlag": "OneBestScore",
        "--outSAMreadID": "Standard",
        "--outSAMmapqUnique": 255,
        "--outSAMflagOR": 0,
        "--outSAMflagAND": 65535,
        "--outSAMfilter": "None",
        "--outSAMmultNmax": -1,
        "--outSAMtlen": 1,
        "--outBAMcompression": 1,
        "--outBAMsortingThreadN": 0,
        "--outBAMsortingBinsN": 50,
        "--bamRemoveDuplicatesMate2basesN": 0,
        "--outWigType": "None",
        "--outWigStrand": "Stranded",
        "--outWigNorm": "RPM",
        "--outFilterType": "Normal",
        "--outFilterMultimapScoreRange": 1,
        "--outFilterMultimapNmax": 10,
        "--outFilterMismatchNmax": 10,
        "--outFilterMismatchNoverLmax": 0.3,
        "--outFilterMismatchNoverReadLmax": 1.0,
        "--outFilterScoreMin": 0,
        "--outFilterScoreMinOverLread": 0.66,
        "--outFilterMatchNmin": 0,
        "--outFilterMatchNminOverLread": 0.66,
        "--outFilterIntronMotifs": "None",
        "--outFilterIntronStrands": "RemoveInconsistentStrands",
        "--outSJfilterReads": "All",
        "--outSJfilterOverhangMin": [30, 12, 12, 12, 12],
        "--outSJfilterCountUniqueMin": [3, 1, 1, 1, 1],
        "--outSJfilterCountTotalMin": [3, 1, 1, 1, 1],
        "--outSJfilterDistToOtherSJmin": [10, 0, 5, 10, 10],
        "--outSJfilterIntronMaxVsReadN": [50000, 100000, 200000, 200000],
        "--scoreGap": 0,
        "--scoreGapNoncan": -8,
        "--scoreGapGCAG": -4,
        "--scoreGapATAC": -8,
        "--scoreGenomicLengthLog2scale": -0.25,
        "--scoreDelOpen": -2,
        "--scoreDelBase": -2,
        "--scoreInsOpen": -2,
        "--scoreInsBase": -2,
        "--scoreStitchSJshift": 1,
        "--seedSearchStartLmax": 50,
        "--seedSearchStartLmaxOverLread": 1.0,
        "--seedSearchLmax": 0,
        "--seedMultimapNmax": 10000,
        "--seedPerReadNmax": 1000,
        "--seedPerWindowNmax": 50,
        "--seedNoneLociPerWindow": 10,
        "--seedSplitMin": 12,
        "--seedMapMin": 5,
        "--alignIntronMin": 21,
        "--alignIntronMax": 0,
        "--alignMatesGapMax": 0,
        "--alignSJoverhangMin": 5,
        "--alignSJstitchMismatchNmax": [0, -1, 0, 0, 0],
        "--alignSJDBoverhangMin": 3,
        "--alignSplicedMateMapLmin": 0,
        "--alignSplicedMateMapLminOverLmate": 0.66,
        "--alignWindowsPerReadNmax": 10000,
        "--alignTranscriptsPerWindowNmax": 100,
        "--alignTranscriptsPerReadNmax": 10000,
        "--alignEndsType": "Local",
        "--alignEndsProtrude": [0, "ConcordantPair"],
        "--alignSoftClipAtReferenceEnds": "Yes",
        "--alignInsertionFlush": "None",
        "--peOverlapNbasesMin": 0,
        "--peOverlapMMp": 0.01,
        "--winAnchorMultimapNmax": 50,
        "--winBinNbits": 16,
        "--winAnchorDistNbins": 9,
        "--winFlankNbins": 4,
        "--winReadCoverageRelativeMin": 0.5,
        "--winReadCoverageBasesMin": 0,
        "--chimOutType": "Junctions",
        "--chimSegmentMin": 0,
        "--chimScoreMin": 0,
        "--chimScoreDropMax": 20,
        "--chimScoreSeparation": 10,
        "--chimScoreJunctionNonGTAG": -1,
        "--chimJunctionOverhangMin": 20,
        "--chimSegmentReadGapMax": 0,
        "--chimFilter": "banGenomicN",
        "--chimMainSegmentMultNmax": 10,
        "--chimMultimapNmax": 0,
        "--chimMultimapScoreRange": 1,
        "--chimNonchimScoreDropMin": 20,
        "--chimOutJunctionFormat": 0,
        "--quantTranscriptomeBAMcompression": 1,
        "--quantTranscriptomeBan": "IndelSoftclipSingleend",
        "--twopassMode": "None",
        "--twopass1readsN": -1,
        "--waspOutputMode": "None",
        "--soloType": "None",
        "--soloCBstart": 1,
        "--soloCBlen": 16,
        "--soloUMIstart": 17,
        "--soloUMIlen": 10,
        "--soloBarcodeReadLength": 1,
        "--soloAdapterMismatchesNmax": 1,
        "--soloCBmatchWLtype": "1MM_multi",
        "--soloStrand": "Forward",
        "--soloFeatures": "Gene",
        "--soloUMIdedup": "1MM_All",
        "--soloOutFileNames": ["Solo.out/", "features.tsv", "barcodes.tsv", "matrix.mtx"],
        "--soloCellFilter": ["CellRanger2.2", 3000, 0.99, 10, 10],
        "--soloOutFormatFeaturesGeneField3": ["Gene", "Expression"]
    },
    "toolshed.g2.bx.psu.edu/repos/devteam/cufflinks/cufflinks/2.2.1.3":
    {
        "-o": "./",
        "--output-dir": "./",
        "-p": 1,
        "--num-threads": 1,
        "--seed": 0,
        "-m": 200,
        "--frag-len-mean": 200,
        "-s": 80,
        "--frag-len-std-dev": 80,
        "--max-mle-iterations": 5000,
        "--num-frag-count-draws": 100,
        "--num-frag-assign-draws": 50,
        "-L": "CUFF",
        "--label": "CUFF",
        "-F": 0.10,
        "--min-isoform-fraction": 0.10,
        "-j": 0.15,
        "--pre-mrna-fraction": 0.15,
        "-I": 300000,
        "--max-intron-length": 300000,
        "-a": 0.001,
        "--junc-alpha": 0.001,
        "-A": 0.09,
        "--small-anchor-fraction": 0.09,
        "--min-frags-per-transfrag": 10,
        "--overhang-tolerance": 8,
        "--max-bundle-length": 3500000,
        "--max-bundle-frags": 500000,
        "--min-intron-length": 50,
        "--trim-3-avgcov-thresh": 10,
        "--trim-3-dropoff-frac": 0.1,
        "--max-multiread-fraction": 0.75,
        "--overlap-radius": 50,
        "--3-overhang-tolerance": 600,
        "--intron-overhang-tolerance": 30
    }
}


def simplify_command_line(job_info):
    if job_info['tool_id'] not in default_parameters:
        return job_info['command_line']
    current_defaults = default_parameters[job_info['tool_id']]
    command_line_split = re.split(' +', job_info['command_line'])
    indices_to_remove = []
    for i, item in enumerate(command_line_split):
        if item in current_defaults:
            if not isinstance(current_defaults[item], list):
                if command_line_split[i + 1].strip("'") == str(current_defaults[item]):
                    indices_to_remove.append(i)
                    indices_to_remove.append(i + 1)
            else:
                all_match = True
                current_indices = [i]
                for k, val in enumerate(current_defaults[item]):
                    if command_line_split[i + 1 + k].strip("'") == str(val):
                        current_indices.append(i + 1 + k)
                    else:
                        all_match = False
                        break
                if all_match:
                    indices_to_remove += current_indices
        elif '=' in item:
            potential_key = item.split('=')[0]
            potential_value = '='.join(item.split('=')[1:])
            if potential_key in current_defaults \
               and potential_value.strip("'") == str(current_defaults[potential_key]):
                indices_to_remove.append(i)
    return ' '.join([item for i, item in enumerate(command_line_split)
                     if i not in indices_to_remove])


def update_tables(gi, dataset_id, simplify, replacement_table={}, visited_dataset_ids=[], command_lines_rev_order=[]):
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
            if simplify:
                command_lines_rev_order.append(prefix + simplify_command_line(job_info))
            else:
                command_lines_rev_order.append(prefix + job_info['command_line'])
            visited_dataset_ids.append(dataset_id)
            inputs_ids = [o['id'] for o in job_info['inputs'].values()]
            for iid in inputs_ids:
                replacement_table, visited_dataset_ids, command_lines_rev_order = update_tables(gi, iid, simplify, replacement_table, visited_dataset_ids, command_lines_rev_order)
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
    argp.add_argument('--simplify', action="store_true",
                      help="Remove parameters with default values")
    return(argp)


def main(args=None):
    args = parse_arguments().parse_args(args)
    gi = GalaxyInstance(args.url, key=args.api)
    replacement_table, visited_dataset_ids, \
        command_lines_rev_order = update_tables(gi, args.datasetID, args.simplify)

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
