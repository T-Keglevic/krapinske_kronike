from PIL import Image
import os

# === CONFIG ===
SRC_FOLDER = "images_fullres"  # folder with your original images
DST_FOLDER = "images"          # folder for GitHub-ready compressed images
MAX_DIM = 2000                 # max width or height in pixels
QUALITY = 50                   # JPG quality (0-100)

# === CREATE DESTINATION FOLDER IF IT DOESN'T EXIST ===
os.makedirs(DST_FOLDER, exist_ok=True)

# === PROCESS IMAGES ===
count = 0
for filename in os.listdir(SRC_FOLDER):
    if filename.lower().endswith(".jpg"):
        src_path = os.path.join(SRC_FOLDER, filename)
        dst_path = os.path.join(DST_FOLDER, filename)

        try:
            with Image.open(src_path) as im:
                # Resize if bigger than MAX_DIM
                im.thumbnail((MAX_DIM, MAX_DIM))

                # Save compressed
                im.save(dst_path, quality=QUALITY, optimize=True)
                count += 1

        except Exception as e:
            print(f"Failed: {filename} -> {e}")

print(f"✅ Finished compressing {count} images into '{DST_FOLDER}' folder.")
