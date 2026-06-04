# 방법
# 1. 사진을 직접 올린다. (base64 인코딩)
# 2. 이미지 URL을 주고 읽어가라고 한다.

import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

image_url = 

def encode_image(path):
    with open(path, 'rb') as f:
        return base64.b64

def ask_about_image(question, b64):

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {
            "role": 'user',
            "type": 'image_url', 'image_url': {'url': f''}

    }])

    return response.choices[0].message.content

questions = [
    # "이미지에 있는 한글 글자를 다 읽어줘",
    # "해당 이미지 사용된 주요 색상을 알려줘",
    # "이미지의 전체 분위기를 한 문장으로 표현하면?"
    "이 주식 차트를 보고 어떤 종목인지 알려주고 기술적 분석을 해줘",
    "이 주식 차트를 보고 골든 크로스와 데드 크로스 시점을 알려줘",
    "이 주식 차트를 보고 매수 또는 매도 타이밍을 분석해주고 왜 그런지 기술적으로 설명해줘"
]

b64 = encode_image(image_url)
for q in questions:
    print('-'*60)
    print(f'질문: {q}')
    print(f'답변: {ask_about_image(q, b64)}')