import argparse
from enum import unique
import json
import os
import random
import pandas as pd
import math
from tqdm import tqdm

def get_unique(meta_json):
    unique_id = {}
    video_to_skin = {}
    for k, v in meta_json.items():
        if v["casual_conv_subject_id"] not in unique_id.keys():
            unique_id[v["casual_conv_subject_id"]] = []
        video_to_skin[k[:-4]] = int(v["casual_conv_label"]["skin-type"])
        unique_id[v["casual_conv_subject_id"]].append(k)

    # Validating
    return unique_id, video_to_skin

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

print(f"len data: {len(data)}")

# Take samples from buckets
# unique_id = {user id, list[video names]}
unique_id, video_to_skin = get_unique(data)
# fold_video = {video names, fold number}
fold_videos = {}
print(f"len unique id: {len(unique_id)}")

num_subj_id_in_split = int(len(unique_id) / args.n_splits)
# print(f"num subj ids splits: {num_subj_id_in_split}")
for fold in range(args.n_splits):
    end = None if fold == args.n_splits-1 else (fold+1)*num_subj_id_in_split
    subj_fold = list(unique_id.keys())[fold*num_subj_id_in_split : end]

    for subj_id in subj_fold:
        for vid in unique_id[subj_id]:
            fold_videos[vid[:-4]] = fold

print("fold_videos", len(fold_videos))
print(f"video to skin: {len(video_to_skin)}")

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
            fold_data.append([video, file, label, ori_vid, int(file.split("_")[0]), fold, video_to_skin[video]])


random.shuffle(fold_data)
pd.DataFrame(fold_data, columns=["video", "file", "label", "original", "frame", "fold", "skin_tag"]).to_csv(args.out, index=False)