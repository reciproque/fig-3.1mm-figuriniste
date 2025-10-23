from PIL import Image
import itertools
import os

columns = {
    # 1:"bras",
    1: "peau",
    2: "cheveux",
    3: "robe",
    4: "armoiries"
}

output_dir = "resultats"
os.makedirs(output_dir, exist_ok=True)

images_by_col = {}
for col, path in columns.items():
    files = sorted([
        os.path.join(path, f) for f in os.listdir(path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
    if not files:
        raise ValueError(f"Aucune image trouvée dans le dossier : {path}")
    images_by_col[col] = files

combinations = itertools.product(
    range(1, len(images_by_col[1]) + 1),
    range(1, len(images_by_col[2]) + 1),
    range(1, len(images_by_col[3]) + 1),
    range(1, len(images_by_col[4]) + 1),
    # range(1, len(images_by_col[5]) + 1)
)

for combo in combinations:
    combo_name = "".join(map(str, combo))
    output_path = os.path.join(output_dir, f"{combo_name}.png")

    base = Image.open(images_by_col[1][combo[0]-1]).convert("RGBA")

    for i, idx in enumerate(combo[1:], start=2):
        overlay = Image.open(images_by_col[i][idx-1]).convert("RGBA")
        if overlay.size != base.size:
            overlay = overlay.resize(base.size)
        base = Image.alpha_composite(base, overlay)

    base.save(output_path)
