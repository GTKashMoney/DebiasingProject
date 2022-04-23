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
# unique_id = {user id, list[video names]}
unique_id, skin_hist = get_unique(data)
# fold_video = {video names, fold number}
fold_videos = {}

num_subj_id_in_split = int(len(unique_id) / args.n_splits)
# print(len(unique_id))
for fold in range(args.n_splits):
    end = (fold+1)*num_subj_id_in_split
    subj_fold = list(unique_id.keys())[fold*num_subj_id_in_split:end if end < len(unique_id) else len(unique_id)]
    # list[user id]
    # print(len(subj_fold))

    for subj_id in subj_fold:
        for vid in unique_id[subj_id]:
            fold_videos[vid[:-4]] = fold

print("fold_videos", len(fold_videos))

fold_data = []
crops_path = os.path.join(args.root_dir, "crops")
for video in os.listdir(crops_path):
    if video not in fold_videos:
        print("Not in here")
    # print(video)
    label = int(data[video+".mp4"]["is_fake"])
    ori_vid = video

    dirs = os.listdir(os.path.join(crops_path, video))
    fold = fold_videos[video]
    for file in dirs:
        if file.endswith(".png"):
            fold_data.append([video, file, label, ori_vid, int(file.split("_")[0]), fold])


random.shuffle(fold_data)
pd.DataFrame(fold_data, columns=["video", "file", "label", "original", "frame", "fold"]).to_csv(args.out, index=False)