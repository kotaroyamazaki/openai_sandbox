import datetime
import os
from os.path import join, dirname
from image_io import convert_rgba, save_image
from openai import OpenAI
import os


client = OpenAI()

# 入力画像のパス
input_original_path = "inputs/r.png"
input_mask_path = "inputs/mask_r.png"
# input_original_pathとinput_mask_pathの画像を開いて画像が 'RGBA' モードでない場合にのみ変換を行う
convert_rgba(input_original_path)
convert_rgba(input_mask_path)

response = client.images.edit(
    model="dall-e-2",
    image=open(input_original_path, "rb"),
    mask=open(input_mask_path, "rb"),
    prompt="A sunlit indoor lounge area with a pool containing a penguin",
    n=1,
    size="1024x1024"
)

results = response.data
save_image(results, "outputs")
