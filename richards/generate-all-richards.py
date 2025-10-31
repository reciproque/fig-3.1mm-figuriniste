from PIL import Image
import itertools
import os


for bras in range(1,4):

    columns = {
        1: "richards/bras"+str(bras)+"/peau",
        2: "richards/bras"+str(bras)+"/cheveux",
        3: "richards/bras"+str(bras)+"/robe",
        4: "richards/bras"+str(bras)+"/armoiries"
    }

    output_dir = "richards/resultats"
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
        range(1, len(images_by_col[4]) + 1))

    for combo in combinations:
        combo_name = "".join(map(str, combo))
        output_path = os.path.join(output_dir, f"{str(bras)+combo_name}.png")

        base = Image.open(images_by_col[1][combo[0]-1]).convert("RGBA")

        for i, idx in enumerate(combo[1:], start=2):
            overlay = Image.open(images_by_col[i][idx-1]).convert("RGBA")
            if overlay.size != base.size:
                overlay = overlay.resize(base.size)
            base = Image.alpha_composite(base, overlay)
            
            # TODO : crop and add overlay Compiègne / background etc
            # left = 155
            # top = 1920
            # right = 360
            # bottom = 0

            # cropped = base.crop((left, top, right, bottom))

        base.save(output_path)
