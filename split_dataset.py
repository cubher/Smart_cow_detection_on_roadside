import os
import shutil
import random

# Paths
base_dir = "images"
output_dir = "dataset"
train_ratio = 0.8

# Classes
classes = ["cow", "notcow"]

# Create output dirs
for split in ["train", "test"]:
    for cls in classes:
        os.makedirs(os.path.join(output_dir, split, cls), exist_ok=True)

# Split images
for cls in classes:
    src_dir = os.path.join(base_dir, cls)
    all_files = os.listdir(src_dir)
    random.shuffle(all_files)

    split_idx = int(len(all_files) * train_ratio)
    train_files = all_files[:split_idx]
    test_files = all_files[split_idx:]

    for f in train_files:
        shutil.copy(os.path.join(src_dir, f), os.path.join(output_dir, "train", cls, f))
    for f in test_files:
        shutil.copy(os.path.join(src_dir, f), os.path.join(output_dir, "test", cls, f))

print("✅ Dataset split complete! Check the 'dataset' folder.")
