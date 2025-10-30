import csv
import qrcode
from PIL import Image
import os

QR_SIZE_PX = 250  # Taille finale de l'image PNG
BOX_SIZE = 10     
BORDER = 4        

def generate_qr(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=BOX_SIZE,
        border=BORDER,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((QR_SIZE_PX, QR_SIZE_PX), Image.LANCZOS)
    return img

def clean_filename(name):
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in name)

with open("richards/url-qrcodes.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = clean_filename(row['nom'])
        url = row['url']
        qr_img = generate_qr(url)
        filename = f"{name}.png"
        qr_img.save("richards/qrcodes/"+filename)
        print(f"QR code généré : {filename}")