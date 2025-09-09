import os
import requests
from pycocotools.coco import COCO

# -----------------------------
# 1. Setup paths
# -----------------------------
dataDir = "annotations_trainval2017"   # your folder
dataType = "train2017"                 # or "val2017"
annFile = f"F:/Workspace/Smart cow detection on roadside/images/annotations_trainval2017/instances_{dataType}.json"

# -----------------------------
# 2. Load COCO annotations
# -----------------------------
coco = COCO(annFile)

# Get category IDs
cowId = coco.getCatIds(catNms=['cow'])[0]
carId = coco.getCatIds(catNms=['car'])[0]
motoId = coco.getCatIds(catNms=['motorcycle'])[0]

# Get all image IDs for each class
cowImgIds = set(coco.getImgIds(catIds=[cowId]))
carImgIds = set(coco.getImgIds(catIds=[carId]))
motoImgIds = set(coco.getImgIds(catIds=[motoId]))

# Exclude → motorcycle images that do NOT contain cow or car
excludeImgIds = cowImgIds.union(carImgIds)
moto_only_ImgIds = list(motoImgIds.difference(excludeImgIds))
print(f"Found {len(moto_only_ImgIds)} images with motorcycle but NOT cow or car")

# -----------------------------
# 3. Download those images
# -----------------------------
download_dir = f"coco_motorcycle_no_cow_car_{dataType}"
os.makedirs(download_dir, exist_ok=True)

for i, imgId in enumerate(moto_only_ImgIds[:200]):  # limit to 50 for demo
    img = coco.loadImgs(imgId)[0]
    url = img['coco_url']
    filename = os.path.join(download_dir, img['file_name'])
    if not os.path.exists(filename):
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
    print(f"Downloaded {i+1}/{len(moto_only_ImgIds)}: {filename}")
