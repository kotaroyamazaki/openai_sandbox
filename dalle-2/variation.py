from image_io import convert_rgba, save_image
from openai import OpenAI

client = OpenAI()

# 入力画像のパス
image_edit_original_path = "inputs/r.png"
convert_rgba(image_edit_original_path)


response = client.images.create_variation(
    image=open(image_edit_original_path, "rb"),
    n=1,
    size="256x256"
)

results = response.data
save_image(results, "outputs")
