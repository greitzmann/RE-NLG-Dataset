##############################################
# Python script showing how many triples     #
# we have by annotator (with some details)   #
# like how many with dates, coreference, etc #
##############################################

import os
import json
import argparse

annotator_date = "Date_Linker"
annotator_coref = "Simple_Coreference"
annotator_nosub = "NoSubject-Triple-aligner"
annotator_simple = "Simple-Aligner"
annotator_SPO = "SPOAligner"

stats = {
        "NoSubj_all" : 0,
        "NoSubj_dates" : 0,
        "Simple_all" : 0,
        "Simple_coref" : 0,
        "Simple_dates" : 0,
        "SPO_all" : 0,
        "SPO_coref" : 0,
        "SPO_dates" : 0
        }

parser = argparse.ArgumentParser(description='filter extracted attributes')
parser.add_argument('-i', '--input', help='input folder name containing the processed dataset', required=True)
parser.add_argument('-o', '--out', help='output file name', required=True)
args = parser.parse_args()

result = args.out
path_to_json = args.input

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for c, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        print "Starting the file : " + str(os.path.join(path_to_json, js)) + " .. %s / %s" % (c+1, len(json_files))
        for d in json.load(json_file):
            for t in d['triples']:
                if t['annotator'] == annotator_nosub:
                    stats['NoSubj_all'] += 1
                    if t['subject']['annotator'] == annotator_date or t['object']['annotator'] == annotator_date:
                        stats['NoSubj_dates'] += 1
                elif t['annotator'] == annotator_simple:
                    stats['Simple_all'] += 1
                    if t['subject']['annotator'] == annotator_coref or t['object']['annotator'] == annotator_coref:
                        stats['Simple_coref'] += 1
                    if t['subject']['annotator'] == annotator_date or t['object']['annotator'] == annotator_date:
                        stats['Simple_dates'] += 1
                elif t['annotator'] == annotator_SPO:
                    stats['SPO_all'] += 1
                    if t['subject']['annotator'] == annotator_coref or t['object']['annotator'] == annotator_coref:
                        stats['SPO_coref'] += 1
                    if t['subject']['annotator'] == annotator_date or t['object']['annotator'] == annotator_date:
                        stats['SPO_dates'] += 1

with open(result, 'w') as k:
    k.write(json.dumps(stats, indent=4))
