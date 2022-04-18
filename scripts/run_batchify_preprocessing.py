from json import detect_encoding
import os
import subprocess
import numpy as np

num_batches = 159

# Run Selim's Preprocessing scripts (certain parts) for each batch.
DATA_ROOT = "/dataset/"

metadata_name = "metadata.json"
temp_metadata_name = "garbage.nosj"
batch_folder_prefix = "batch_"
crops_dir = 'crops'
folds_file = 'folds.csv'

detect_orig_faces_py = '/workspace/preprocessing/detect_original_faces.py'
extract_crops_py = '/workspace/preprocessing/extract_crops.py'
generate_landmarks_py = '/workspace/preprocessing/generate_landmarks.py'
generate_diffs_py = '/workspace/preprocessing/generate_diffs.py'
generate_folds_py = '/workspace/preprocessing/generate_folds.py'

run_detect_orig_face = False
run_extract_crops = False
run_extract_landmarks = False
run_extract_ssim = False
run_generate_folds = False

# Rename all metadatas to temps
for batch_num in range(num_batches):
    file_old_path = os.path.join(DATA_ROOT, F"{batch_folder_prefix}{batch_num}", metadata_name)
    file_new_path = os.path.join(DATA_ROOT, F"{batch_folder_prefix}{batch_num}", temp_metadata_name)

    if os.path.exists(file_old_path):
        os.rename(file_old_path, file_new_path)

for batch_num in range(num_batches):
    print(f"Processing batch: {batch_num}")
    if batch_num > 0:
        # Rename previous batch file we just used to temp name
        file_old_path = os.path.join(DATA_ROOT, F"{batch_folder_prefix}{batch_num-1}", metadata_name)
        file_new_path = os.path.join(DATA_ROOT, F"{batch_folder_prefix}{batch_num-1}", temp_metadata_name)
        os.rename(file_old_path, file_new_path)

    # Rename current batch metadata from temp name to real name so that it is used in processing
    file_old_path = os.path.join(DATA_ROOT, F"{batch_folder_prefix}{batch_num}", temp_metadata_name)
    file_new_path = os.path.join(DATA_ROOT, F"{batch_folder_prefix}{batch_num}", metadata_name)
    os.rename(file_old_path, file_new_path)
    print(f"metadata file: {file_new_path}")

    if run_detect_orig_face:
        print("spawning detect original faces subprocess...")
        subprocess.run(['python', detect_orig_faces_py, '--root-dir', DATA_ROOT])
        print("Finished subprocess...")

    if run_extract_crops:
        print("spawning extract crops subprocess...")
        subprocess.run(['python', extract_crops_py, '--root-dir', DATA_ROOT, '--crops-dir', crops_dir])
        print("Finished subprocess...")

    if run_extract_landmarks:
        print("spawning extract landmarks subprocess...")
        subprocess.run(['python', generate_landmarks_py, '--root-dir', DATA_ROOT])
        print("Finished subprocess...")




# Rename all metadatas to originals
for batch_num in range(num_batches):
    file_old_path = os.path.join(DATA_ROOT, F"{batch_folder_prefix}{batch_num}", temp_metadata_name)
    file_new_path = os.path.join(DATA_ROOT, F"{batch_folder_prefix}{batch_num}", metadata_name)

    if os.path.exists(file_old_path):
        os.rename(file_old_path, file_new_path)


# *Can't run these in batchify mode, need to access all videos at once 
# for orig/fake video pairings... need workaround.

# This does a comparison between original video and fake video
if run_extract_ssim:
    print("spawning extract ssim subprocess...")
    subprocess.run(['python', generate_diffs_py, '--root-dir', DATA_ROOT])
    print("Finished subprocess...")

if run_generate_folds:
    print("spawning generate folds subprocess...")
    subprocess.run(['python', generate_folds_py, '--root-dir', DATA_ROOT, '--out', folds_file])
    print("Finished subprocess...")