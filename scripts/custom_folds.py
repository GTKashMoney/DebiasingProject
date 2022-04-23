import argparse
from enum import unique
import json
import os
import random
import pandas as pd
from tqdm import tqdm

def get_unique(meta_json):
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
    return unique_id, skin_hist

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--root-dir", help="root directory", default="/dataset")
arg_parser.add_argument("--out", type=str, default="folds.csv", help="CSV file to save")
arg_parser.add_argument("--seed", type=int, default=777, help="Seed to split, default 777")
arg_parser.add_argument("--n_splits", type=int, default=6, help="Num folds, default 10")
arg_parser.add_argument('-f', metavar='<DFDC input json>', type=str,
                        help='The DFDC test set metadata json file. Defaults to dfdc_metadata.json')
args = arg_parser.parse_args()

metadata = "metadata.json"
if args.f is not None:
    metadata = args.f

with open(metadata, "r") as file:
    data = json.load(file)

# Take samples from buckets
unique_id, skin_hist = get_unique(data)
fold_videos = {}

num_subj_id_in_split = len(unique_id) / args.n_splits
for fold in range(args.n_splits):
    subj_fold = list(unique_id.keys())[fold*num_subj_id_in_split:(fold+1)*num_subj_id_in_split]

    for i in range(len(subj_fold)):
        fold_videos[subj_fold[i][:-4]] = fold


fold_data = []
for k, v in data.items():
    video = k[:-4]
    label = v["is_fake"]
    ori_vid = video

    dirs = os.listdir(os.path.join(args.root_dir, "crops", k[:-4]))
    fold = fold_videos[video]
    for file in dirs:
        fold_data.append([video, file, label, ori_vid, int(file.split("_")[0]), fold])


random.shuffle(fold_data)
pd.DataFrame(fold_data, columns=["video", "file", "label", "original", "frame", "fold"]).to_csv(args.out, index=False)