# image_io.py
import os
from PIL import Image
import requests
import datetime
import base64


def convert_rgba(image_path):
    with Image.open(image_path) as img:
        if img.mode != "RGBA":
            img = img.convert("RGBA")
            img.save(image_path)
    return img


def save_image(results, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i, result in enumerate(results):
        filename = f"{output_dir}/{datetime.datetime.now().isoformat()}.png"
        with open(filename, "wb") as f:
            f.write(requests.get(result.url).content)
        print("Saved to", filename)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
