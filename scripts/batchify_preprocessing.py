import argparse
import json
import os
import numpy as np

batch_size = 25
videos_dir = "train"
batch_dirs_prefix = "batch_"
out_dirs_prefix = "dfdc_train_"
in_metadata = "metadata.json"
train_folder = "train"
test_folder = "test"
unbatchify = False

working_dir = os.path.dirname(os.path.realpath(__file__))
print(f"Working directory: {working_dir}")

# Read metadata
f = open(os.path.join(working_dir, train_folder, in_metadata))
metadata = json.load(f)
f.close()

print(f"len metadata: {len(metadata)}")
print(f"batch_size: {batch_size}")
num_batches = int(np.ceil(len(metadata) / batch_size))
print(f"computed num batches: {num_batches}")

# Create metadata batches
batched_metadata = [None] * num_batches
for n in range(num_batches):
    # Slice elements from metadata
    slice_start = n*batch_size
    slice_end = slice_start + batch_size
    metadata_slice = dict(list(metadata.items())[slice_start:slice_end])
    batched_metadata[n] = metadata_slice

# Make folder for each batch
dirs = [f"{batch_dirs_prefix}{i}" for i in range(num_batches)]
print(f"Creating Batch Dirs: {dirs}")
for dir in dirs:
    dir_path = os.path.join(working_dir, dir)
    os.makedirs(dir_path, exist_ok=True)

# Unbatchify first before moving videos
if unbatchify:
    print(f"Performing unbatchify...")
    train_dir = os.path.join(working_dir, train_folder)
    for dir in dirs:
        batch_dir = os.path.join(working_dir, dir)
        vid_files = os.listdir(batch_dir)
        vid_files.remove('metadata.json')

        for file in vid_files:
            old_file_path = os.path.join(batch_dir, file)
            new_file_path = os.path.join(train_dir, file)

            if os.path.exists(old_file_path):
                os.replace(old_file_path, new_file_path)
    print(f"Unbatchify complete exiting...")
    exit(0)

# Move each video to corresponding batch directory
for i in range(len(batched_metadata)):
    batch_dic = batched_metadata[i]

    for k, v in batch_dic.items():
        vid = k
        old_file_path = os.path.join(working_dir, train_folder, vid)
        new_file_path = os.path.join(working_dir, dirs[i], vid)

        # Move video if it exists
        if os.path.exists(old_file_path):
            os.replace(old_file_path, new_file_path)

    # Write corresponding batch metadata
    batch_meta_path = os.path.join(working_dir, dirs[i], 'metadata.json')
    batch_meta_fp = open(batch_meta_path, 'w+')
    json.dump(batch_dic, batch_meta_fp)

# Next run run_batchify_preprocessing.py