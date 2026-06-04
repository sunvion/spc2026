import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

text = "안녕하세요, OpenAI의 음성 생성 예제입니다. 한국말을 얼마나 잘하는지 확인중입니다."

response = client.audio.speech.create(
    model='tts-1',
    voice='alloy', # 다양한 목소리
    input=text
)

response.write_to_file("output.mp3")
print('저장완료')