import json
import argparse
import os
import numpy as np

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-f', metavar='<DFDC input json>', type=str,
                        help='The DFDC test set metadata json file. Defaults to dfdc_metadata.json')
args = arg_parser.parse_args()

metadata = "metadata.json"
if args.f is not None:
    metadata = args.f

with open(metadata, "r") as file:
    data = json.load(file)
    print(type(data))

    for k, v in data.items():
        v["original"] = None

with open(metadata, "w+") as file:
    json.dump(data, file)