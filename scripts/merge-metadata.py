"""
Script that merges the metadata from the Casual Conversations (CC) dataset with the
metadata for the Deep Fake Detection Challenge (DFDC) test set.

This is needed to be able to use the skin-type label with the DFDC dataset.

# Possible script arguments
-di <inputfile>
    The DFDC test set metadata json file
    Defaults to dfdc_metadata.json
-ci <inputfile>
    The CC test set metadata json file with the correspondences
    defaults to correspondences.json
-o <outputfile>
    The output file with the merged metadata
    Defaults to metadata.json
"""

import argparse
import json
import os
import sys
import numpy as np

###
### Parse Arguments
###

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--di', metavar='<DFDC input json>', type=str,
                        help='The DFDC test set metadata json file. Defaults to dfdc_metadata.json')
arg_parser.add_argument('--ci', metavar='<CC input json>', type=str,
                        help='The CC metadata json file with the CC-DFDC correspondences. Defaults to correspondences.json')
arg_parser.add_argument('--o', metavar='<output file>', type=str,
                        help='The output file with the merged metadata. Defaults to metadata.json')
args = arg_parser.parse_args()


dfdc_metadata = args.di
cc_metadata = args.ci
output_file = args.o


###
### Running script
###

script_header = """
========================================================================
Running merge-metadata.py
========================================================================"""
script_footer = """merge-metadata.py exiting...
========================================================================"""

print(script_header)

# Set defaults if params not provided
used_def_out_arg = False
if args.di is None:
    dfdc_metadata = "dfdc_metadata.json"
if args.ci is None:
    cc_metadata = "correspondences.json"
if args.o is None:
    # keep track if default was used to make sure user wants
    # to ovewrite any existing output file with the same name
    used_def_out_arg = True
    output_file = "metadata.json"

# Validate arguments
valid_files = True
if not os.path.exists(dfdc_metadata):
    valid_files = False
    print(f"{dfdc_metadata} file does not exist")
if not os.path.exists(cc_metadata):
    valid_files = False
    print(f"{cc_metadata} file does not exist")
if not valid_files:
    print(script_footer)
    exit(1)

print(f"Using following files:")
print(f"DFDC Metadata: {dfdc_metadata}")
print(f"CC Metadata: {cc_metadata}")
print(f"Output File: {output_file}")

df_file = open(dfdc_metadata, 'r')
dfdc_json = json.loads(df_file.read())

cc_file = open(cc_metadata, 'r')
cc_json = json.loads(cc_file.read())

# Respect dfdc test set ordering
output_dict = {}
for dfdc_key in dfdc_json.keys():
    # Start with copy of dfdc metadata
    output_dict[dfdc_key] = dfdc_json[dfdc_key]

    # Add cc data to dfdc copy
    for cc_key, cc_val in cc_json[dfdc_key].items():
        output_dict[dfdc_key][cc_key] = cc_val

# Write to output file
output_fp = open(output_file, 'w+')
json.dump(output_dict, output_fp)

print(f"Merge operation complete")
print(script_footer)
