import datetime
import os
from os.path import join, dirname
from image_io import convert_rgba, save_image
from openai import OpenAI
from dotenv import load_dotenv
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
convert_rgba(input_original_path)
convert_rgba(input_mask_path)

response = client.images.edit(
    model="dall-e-2",
    image=open("inputs/original.png", "rb"),
    mask=open("inputs/mask.png", "rb"),
    prompt="A sunlit indoor lounge area with a pool containing a penguin",
    n=1,
    size="1024x1024"
)

result = response.data
save_image([result], "outputs")
