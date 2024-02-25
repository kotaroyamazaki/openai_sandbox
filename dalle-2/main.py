import datetime
import os
from os.path import join, dirname
import requests
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import os


load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# .env の読み込み
load_dotenv()

# .env から環境変数を読み込む
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

# 入力画像のパス
input_original_path = "inputs/original.png"
input_mask_path = "inputs/mask.png"

# input_original_pathとinput_mask_pathの画像を開いて画像が 'RGBA' モードでない場合にのみ変換を行う
with Image.open(input_original_path) as img:
    if img.mode != "RGBA":
        img = img.convert("RGBA")
        img.save(input_original_path)

with Image.open(input_mask_path) as img:
    if img.mode != "RGBA":
        img = img.convert("RGBA")
        img.save(input_mask_path)

response = client.images.edit(
    model="dall-e-2",
    image=open("inputs/original.png", "rb"),
    mask=open("inputs/mask.png", "rb"),
    prompt="A sunlit indoor lounge area with a pool containing a penguin",
    n=1,
    size="1024x1024"
)

image_url = response.data[0].url

# local のoutputsフォルダに保存する
os.makedirs("outputs", exist_ok=True)
# ファイル名は実行日時を使う
filename = f"outputs/{datetime.datetime.now().isoformat()}.png"

with open(filename, "wb") as f:
    f.write(requests.get(image_url).content)
print("Saved to", filename)
