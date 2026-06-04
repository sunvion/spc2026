# 텍스트를 기반으로 이미지를 생성 (GAN)

# 구버전 모델이 dall-e => dall-e-2 => ??
# gpt-image-1.5 또는 gpt-image-2

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

prompt = """노을 지는 해변,
잔잔한 파도,
수채화 스타일,
고해상도,
따뜻한 색감"""

result = client.images.generate(
    model = "gpt-image-1.5",
    prompt = prompt,
    size = "1024x1536",
    quality = "medium", # low / medium / high / auto
)

# image =  

b64 = result.data[0].b64_json
with open('output.png', 'wb') as f:
    f.write(base64.b64decode(b64))

print("저장 완료")