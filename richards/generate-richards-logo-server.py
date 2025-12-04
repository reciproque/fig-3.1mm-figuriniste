import os
from PIL import Image

INPUT_DIR = "richards/resultats"
OUTPUT_DIR = "richards/resultats-serveur"

BACKGROUND_PATH = "richards/background.png"
OVERLAY_PATH = "richards/overlay.png"
FINAL_W, FINAL_H = 1080, 1920

os.makedirs(OUTPUT_DIR, exist_ok=True)

background = Image.open(BACKGROUND_PATH).convert("RGBA")
overlay = Image.open(OVERLAY_PATH).convert("RGBA")


for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    img = Image.open(os.path.join(INPUT_DIR, filename)).convert("RGBA")
    src_w, src_h = img.size

    src_ratio = src_w / src_h
    target_ratio = FINAL_W / FINAL_H
    if src_ratio > target_ratio:
        scale = FINAL_H / src_h
    else:
        scale = FINAL_W / src_w

    new_w = int(src_w * scale)
    new_h = int(src_h * scale)

    resized = img.resize((new_w, new_h), Image.LANCZOS)

    left = (new_w - FINAL_W) // 2
    top = (new_h - FINAL_H) // 2
    right = left + FINAL_W
    bottom = top + FINAL_H

    cropped = resized.crop((left, top, right, bottom))

    composed = background.copy()
    composed.paste(cropped, (0, 0), cropped)
    composed.paste(overlay, (0, 0), overlay)

    composed.convert("RGB").save(
        os.path.join(OUTPUT_DIR, filename),
        quality=95
    )

    print("✔", filename, "OK")


print("Terminé.")