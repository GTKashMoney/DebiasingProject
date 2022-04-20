import argparse
import json
import os
import sys
import numpy as np

from collections import Counter

"""
Prints out dfdc dataset information associated with the given metadata.json

# Possible script arguments
-f <inputfile>
    Defaults to metadata.json
"""


###
### Parse Arguments
###

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--f', metavar='<DFDC input json>', type=str,
                        help='The DFDC test set metadata json file. Defaults to dfdc_metadata.json')
args = arg_parser.parse_args()

###
### Running script
###

script_header = """
========================================================================
Running get-data-statistics.py
========================================================================"""
script_footer = """get-data-statistics.py exiting...
========================================================================"""

print(script_header)

metadata = "metadata.json"
if args.f is not None:
    metadata = args.f

valid_files = True
if not os.path.exists(metadata):
    valid_files = False
    print(f"{metadata} file does not exist")
    print(script_footer)
    exit(1)

print(f"Using metadata file: {metadata}")

df_file = open(metadata, 'r')
meta_json = json.loads(df_file.read())


data_metrics = dict()
data_metrics["names"] = list()
data_metrics["labels"] = list()
data_metrics["skin_types"] = list()
data_metrics["ages"] = list()
data_metrics["genders"] = list()
data_metrics["is_darks"] = list()
data_metrics["subject_ids"] = list()
data_metrics["subject_skins"] = {}
data_metrics["subject_skins_count"] = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}
for k, v in meta_json.items():
    data_metrics["names"].append(k)
    data_metrics["labels"].append(v["label"])
    data_metrics["skin_types"].append(v["casual_conv_label"]["skin-type"])
    data_metrics["ages"].append(v["casual_conv_label"]["age"])
    data_metrics["is_darks"].append(v["casual_conv_label"]["is_dark"])
    data_metrics["genders"].append(v["casual_conv_label"]["gender"])
    data_metrics["subject_ids"].append(v["casual_conv_subject_id"])
    if v["casual_conv_subject_id"] not in data_metrics["subject_skins"].keys():
        data_metrics["subject_skins"][v["casual_conv_subject_id"]] = v["casual_conv_label"]["skin-type"]


for k, v in data_metrics["subject_skins"].items():
    data_metrics["subject_skins_count"][v] += 1

print(f"Total entries: {len(meta_json)}")
print(f"fake vs real {Counter(data_metrics['labels'])}")
print(f"Genders {Counter(data_metrics['genders'])}")
print(f"Unique Subjects {len(set(data_metrics['subject_ids']))}")
print(f"Total Real + Fake: {sum(Counter(data_metrics['labels']).values())}")
print(f"skin type histogram: {Counter(data_metrics['skin_types'])}")
print(f"unique individual skin type histogram: {data_metrics['subject_skins_count']}")
#print(f"ages histogram: {Counter(data_metrics['ages'])}")

# TODO - Plot skin-type histogram

print(f"Showing statistics complete!")
print(script_footer)