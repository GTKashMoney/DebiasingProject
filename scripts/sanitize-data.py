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
                        help='The DFDC test set metadata json file. Defaults to dfdc_metadata.json')
args = arg_parser.parse_args()

###
### Running script
###

script_header = """
========================================================================
Running sanitize-data.py
========================================================================"""
script_footer = """sanitize-data.py exiting...
========================================================================"""

print(script_header)

output_file = "metadata-sanitized.json"
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

bad_entries = []
for k, v in meta_json.items():
    if (v.get("casual_conv_label", None) is None) or (v["casual_conv_label"].get("skin-type", None) is None):
        bad_entries.append(k)

print(f"Number of bad entries (no skin-type): {len(bad_entries)}")

# Remove bad entries from json
for entry in bad_entries:
    del meta_json[entry]

print(f"resulting len of dictionary: {len(meta_json)}")

# Write to output file
output_fp = open(output_file, 'w+')
json.dump(meta_json, output_fp)

print(f"Finished sanitizing - output: {output_file}")
print(script_footer)