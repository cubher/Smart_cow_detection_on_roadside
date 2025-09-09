import os
import hashlib
import random
import string
import time
import shutil

# ✅ Set your target folder here
TARGET_FOLDER = r"F:\Workspace\Smart cow detection on roadside\images\dataset_cows_cleaned"
TEMP_FOLDER = os.path.join(TARGET_FOLDER, "temp")

# Allowed image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

def random_hash(length=12):
    """Generate a random hash-like string."""
    seed = f"{time.time()}_{random.random()}_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}"
    return hashlib.sha1(seed.encode()).hexdigest()[:length]

def rename_and_collect(folder_path):
    for item in os.listdir(folder_path):
        old_path = os.path.join(folder_path, item)

        if os.path.isdir(old_path):
            # Recurse first
            rename_and_collect(old_path)

            # Then rename the folder itself
            if os.path.abspath(old_path) == os.path.abspath(TEMP_FOLDER):
                continue  # skip renaming temp folder

            new_name = random_hash()
            new_path = os.path.join(folder_path, new_name)

            while os.path.exists(new_path):
                new_name = random_hash()
                new_path = os.path.join(folder_path, new_name)

            os.rename(old_path, new_path)
            print(f"Renamed folder: {old_path} -> {new_path}")

        elif os.path.isfile(old_path):
            _, ext = os.path.splitext(item)
            if ext.lower() not in IMAGE_EXTENSIONS:
                continue  # skip non-images

            # Rename image with hash
            new_name = random_hash() + ext.lower()
            new_temp_path = os.path.join(TEMP_FOLDER, new_name)

            while os.path.exists(new_temp_path):
                new_name = random_hash() + ext.lower()
                new_temp_path = os.path.join(TEMP_FOLDER, new_name)

            shutil.move(old_path, new_temp_path)
            print(f"Moved + Renamed file: {old_path} -> {new_temp_path}")

if __name__ == "__main__":
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    rename_and_collect(TARGET_FOLDER)
    print("✅ Recursive renaming + moving to 'temp' completed!")
