import argparse
import json
import os
import pathlib
import sys
import numpy as np


###
### Parse Arguments
###

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--f', metavar='<DFDC input json>', type=str,
                        help='The DFDC test set metadata json file. Defaults to dfdc_metadata.json')
arg_parser.add_argument('--o', metavar='<output file>', type=str,
                        help='The output file with the merged metadata. Defaults to metadata.json')
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
if args.o is not None:
    output_file = args.o

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
    # Check if entry has necessary skin-type label and file exists.
    if ((not os.path.exists(k)) or
            (v.get("casual_conv_label", None) is None) or
            (v["casual_conv_label"].get("skin-type", None) is None)):
        bad_entries.append(k)

print(f"Number of bad entries: {len(bad_entries)}")

working_dir = os.path.dirname(os.path.realpath(__file__))
bad_entries_dir = (pathlib.Path(working_dir).parent).joinpath("bad_entries")
os.makedirs(bad_entries_dir, exist_ok=True)

print(f"Removing bad entries from json and dataset in dir: {working_dir}")
print(f"bad entries dir: {bad_entries_dir}")

# Remove bad entries from json and dataset
for entry in bad_entries:
    # Move out from dataset dir
    old_file_path = os.path.join(working_dir, entry)
    new_file_path = os.path.join(bad_entries_dir, entry)

    if os.path.exists(old_file_path):
        print(f"moved {entry} to bad entries dir")
        os.replace(old_file_path, new_file_path)

    # Remove from metadata
    del meta_json[entry]

print(f"resulting len of dictionary: {len(meta_json)}")

# Write to output file
output_fp = open(output_file, 'w+')
json.dump(meta_json, output_fp)
output_fp.close()

print(f"Finished sanitizing - output file: {output_file}")
print(script_footer)