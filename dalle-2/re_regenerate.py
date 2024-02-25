
from image_io import convert_rgba, save_image, encode_image
from openai import OpenAI
import os
import requests

client = OpenAI()

# OpenAI API Key
api_key = os.environ["OPENAI_API_KEY"]

# 入力画像のパス
image_edit_original_path = "inputs/uniswap_wheel.png"
convert_rgba(image_edit_original_path)

base64_image = encode_image(image_edit_original_path)


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# 画像の説明を生成
# ref: https://platform.openai.com/docs/guides/vision
payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }
    ],
    "max_tokens": 300,
}
response = requests.post(
    "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
response = response.json()

# この結果のChoices -> 0 -> message -> content -> textが画像の説明
# String に変換
explain = response["choices"][0]["message"]["content"]
print(f'画像の説明: {explain}')


# 画像の説明を元に画像を生成
response = client.images.generate(
    model="dall-e-3",
    prompt=explain,
    size="1024x1024",
    quality="standard",
    n=1,
)

save_image(response.data, "outputs")

# さらにプロンプト化する
# URL であればSDKを利用できる
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
          "role": "user",
          "content": [
              {"type": "text", "text": "What’s in this image?"},
              {
                  "type": "image_url",
                  "image_url": {
                      "url": response.data[0].url,
                  },
              },
          ],
        }
    ],
    max_tokens=300,
)

explain = response.choices[0].message.content
print(f'生成された画像の説明: {explain}')

# 画像の説明を元に画像を生成
response = client.images.generate(
    model="dall-e-3",
    prompt=explain,
    size="1024x1024",
    quality="standard",
    n=1,
)

save_image(response.data, "outputs")
