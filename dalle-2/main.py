import datetime
import os
from os.path import join, dirname
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# .env の読み込み
load_dotenv()

# .env から環境変数を読み込む
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

response = client.images.generate(
    model="dall-e-3",
    prompt="a white siamese cat",
    size="1024x1024",
    quality="standard",
    n=1,
)

image_url = response.data[0].url

# local のoutputsフォルダに保存する
os.makedirs("outputs", exist_ok=True)
# ファイル名は実行日時を使う
filename = f"outputs/{datetime.datetime.now().isoformat()}.png"

with open(filename, "wb") as f:
    f.write(requests.get(image_url).content)
print("Saved to", filename)
