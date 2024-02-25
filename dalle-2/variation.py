import os
from os.path import join, dirname
from image_io import convert_rgba, save_image
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# .env から環境変数を読み込む
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

# 入力画像のパス
image_edit_original_path = "inputs/gopher.png"
convert_rgba(image_edit_original_path)


response = client.images.create_variation(
    image=open(image_edit_original_path, "rb"),
    n=3,
    size="256x256"
)

results = response.data
save_image(results, "outputs")
