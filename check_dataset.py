import os
from collections import Counter

DATASET_DIR = "dataset"
CLASSES = ["clear", "slightly_turbid", "turbid"]
EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

for class_name in CLASSES:
    folder = os.path.join(DATASET_DIR, class_name)

    files = [
        f for f in os.listdir(folder)
        if os.path.splitext(f)[1].lower() in EXTENSIONS
    ]

    print(f"{class_name}: {len(files)}")

print(f"Total: {sum(
    len([
        f for f in os.listdir(os.path.join(DATASET_DIR, c))
        if os.path.splitext(f)[1].lower() in EXTENSIONS
    ])
    for c in CLASSES
)}")