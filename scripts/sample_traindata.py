import argparse
import json
import os
from glob import glob
from pathlib import Path
import shutil
import os
from random import sample
from tqdm import tqdm


def get_real_videos(root_dir):
    videos = []
    for json_path in glob(os.path.join(root_dir, "*/metadata.json")):
        dir = Path(json_path).parent
        with open(json_path, "r") as f:
            metadata = json.load(f)
        for k, v in metadata.items():
            label = v["label"]
            if label == "REAL":
                if os.path.exists(os.path.join(root_dir, dir, k)):
                    videos.append({"name": k[:-4], "parent_path": dir})

    return videos

def get_fake_videos(root_dir, real_videos):
    fake_videos = []
    for real in real_videos:
        json_path = glob(os.path.join(root_dir, real["parent_path"], "metadata.json"))[0]
        dir = Path(json_path).parent
        with open(json_path, "r") as f:
            metadata = json.load(f)
        for k, v in metadata.items():
            original = v.get("original", None)
            if not original:
                original = k
            label = v["label"]
            if label == "FAKE":
                if original[:-4] == real["name"]:
                    if os.path.exists(os.path.join(root_dir, dir, k)):
                        fake_videos.append({"name": k[:-4], "parent_path": dir, "original": original})

    return fake_videos

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--root_dir', metavar='train data', type=str)
    args = arg_parser.parse_args()
    
    real_videos = get_real_videos(args.root_dir)
    real_videos = sample(real_videos, 1000)
    # print("Sampled reals:", len(real_videos))
    fake_videos = get_fake_videos(args.root_dir, real_videos)
    # print("Sampled fakes:", len(fake_videos))

    train_path = os.path.join(args.root_dir, "..", "subsample_kaggle", "train")
    os.makedirs(train_path, exist_ok=True)

    # "fzqnoyzhbm.mp4": {
    #     "label": "FAKE",
    #     "split": "train",
    #     "original": "vpmyeepbep.mp4"
    # },
    data = {}
    for real in real_videos:
        data[real["name"]+".mp4"] = {
            "label": "REAL",
            "split": "train"
        }
    # print("Size of data:", len(data))
    for fake in fake_videos:
        data[fake["name"]+".mp4"] = {
            "label": "FAKE",
            "split": "train",
            "original": fake["original"]
        }
    print("Size of data:", len(data))
    with open(os.path.join(train_path, "metadata.json"), "w") as f:
        json.dump(data, f)

    print("Transfering Reals")
    for real in tqdm(real_videos):
        src = os.path.join(args.root_dir, real["parent_path"], real["name"]+".mp4")
        shutil.copy(src, train_path)
    print("Transfering Fakes")
    for fake in tqdm(fake_videos):
        src = os.path.join(args.root_dir, fake["parent_path"], fake["name"]+".mp4")
        shutil.copy(src, train_path)