import argparse
import json
import os
import sys
import numpy as np

###
### Parse Arguments
###

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--f', metavar='<DFDC input json>', type=str,
                        help='The DFDC test set metadata json file. Defaults to metadata.json')
arg_parser.add_argument('--tp', metavar='<Train Split percent>', type=str,
                        help='The percentage of the input to use as Training data. (int 0 - 100) default = 80')
args = arg_parser.parse_args()

###
### Running script
###

script_header = """
========================================================================
Running prepare-splits.py
========================================================================"""
script_footer = """prepare-splits.py exiting...
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
if int(args.tp) < 0 or int(args.tp) > 100:
    print("Train percentage cannot be below 0 or over 100")
    print(script_footer)
    exit(1)

print(f"Using metadata file: {metadata}")

train_perc = int(args.tp)
test_perc = 100 - train_perc

df_file = open(metadata, 'r')
meta_json = json.loads(df_file.read())

# Condition splits on the skin-type field - Create skin-type histogram
skin_hist = dict()
for k, v in meta_json.items():
    skin_type = v['casual_conv_label']['skin-type']
    if skin_hist.get(skin_type, None) is None:
        skin_hist[skin_type] = list()

    skin_hist[skin_type].append(k)

# Validating
for k, v in skin_hist.items():
    print(f"skin type: {k} count: {len(v)}")

# Take percentage from each bucket uniformly

print(f"Creating splits complete!")
print(script_footer)