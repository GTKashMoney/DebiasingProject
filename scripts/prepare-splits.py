import argparse
import json
import os
import pathlib
import shutil
import sys
import numpy as np

from numpy.random import default_rng

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

print(f"Train percentage: {train_perc}")
print(f"Test percentage: {test_perc}")

df_file = open(metadata, 'r')
meta_json = json.loads(df_file.read())

# Condition splits on the skin-type field - Create skin-type histogram
unique_id = {}
skin_hist = {x: [] for x in range(1, 7)}
for k, v in meta_json.items():
    if v["casual_conv_subject_id"] not in unique_id.keys():
        unique_id[v["casual_conv_subject_id"]] = []
        skin_hist[int(v["casual_conv_label"]["skin-type"])].append(v["casual_conv_subject_id"])
    unique_id[v["casual_conv_subject_id"]].append(k)

# Validating
for k, v in skin_hist.items():
    print(f"skin type: {k} count: {len(v)}")

# Take percentage from each bucket uniformly
rng = default_rng(4162022)
test_keys = []
train_keys = []
for i in range(1, 7):
    if (skin_hist.get(i, None) is None) or (len(skin_hist[i]) == 0):
        continue

    keys = skin_hist[i]
    if len(keys) == 1:
        test_keys.append(keys[0])
        continue

    num_test_choices = int((test_perc/100) * len(keys))
    # print(f"num test choices: {num_test_choices}")

    ndxs = rng.permutation(len(keys))
    test_ndxs, train_ndxs = ndxs[:num_test_choices], ndxs[num_test_choices:]

    # print(f"test ndxs: {test_ndxs}")
    # print(f"train ndxs: {train_ndxs}")

    test_choices = np.array(keys)[test_ndxs]
    train_choices = np.array(keys)[train_ndxs]

    # print(f"test choices: {np.array(keys)[test_ndxs]}")
    # print(f"train choices: {np.array(keys)[train_ndxs]}")
    # print(f"test choices len: {len(np.array(keys)[test_ndxs])}")
    # print(f"train choices len: {len(np.array(keys)[train_ndxs])}")

    test_keys += list(test_choices)
    train_keys += list(train_choices)


print(f"test set len: {len(test_keys)}")
print(f"train set len: {len(train_keys)}")

# Split up videos
train_folder = "train"
test_folder = "test"
if os.path.exists(train_folder):
    shutil.rmtree(train_folder)
if os.path.exists(test_folder):
    shutil.rmtree(test_folder)

os.makedirs(train_folder, exist_ok=False)
os.makedirs(test_folder, exist_ok=False)

working_dir = os.path.dirname(os.path.realpath(__file__))

# Move training videos to train set, modify metadata to mark as train
train_metadata = dict()
subj_vid_count = dict()
for subject_id in train_keys:
    for vid in unique_id[subject_id]:
        train_metadata[vid] = meta_json[vid]
        train_metadata[vid]['split'] = "train"

        old_file_path = os.path.join(working_dir, vid)
        new_file_path = os.path.join(working_dir, train_folder, vid)

        if os.path.exists(old_file_path):
            os.replace(old_file_path, new_file_path)
print(f"len train metadata: {len(train_metadata)}")

# Move test videos to test set, modify metadata to mark as test
test_metadata = dict()
for subject_id in test_keys:
    for vid in unique_id[subject_id]:
        test_metadata[vid] = meta_json[vid]
        test_metadata[vid]['split'] = 'test'

        old_file_path = os.path.join(working_dir, vid)
        new_file_path = os.path.join(working_dir, test_folder, vid)

        if os.path.exists(old_file_path):
            os.replace(old_file_path, new_file_path)
print(f"len test metadata: {len(test_metadata)}")

train_meta_path = os.path.join(working_dir, train_folder, 'metadata.json')
test_meta_path = os.path.join(working_dir, test_folder, 'metadata.json')

print(f"Writing train metadata to: {train_meta_path}")
train_meta_fp = open(train_meta_path, 'w+')
json.dump(train_metadata, train_meta_fp)
train_meta_fp.close()

print(f"Writing test metadata to: {test_meta_path}")
test_meta_fp = open(test_meta_path, 'w+')
json.dump(test_metadata, test_meta_fp)
test_meta_fp.close()

print(f"Creating splits complete!")
print(script_footer)