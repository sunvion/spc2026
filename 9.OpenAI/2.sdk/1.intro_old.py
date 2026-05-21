# pip install openai==0.28
import openai

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')

openai.api_key = os.getenv('OPENAI_API_KEY')

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages = [
        {'role': 'system', 'content':'당신은 나의 질문에 대답을 잘하는 쳇봇입니다.'},
        {'role': 'user', 'content':'안녕하세요, 반갑습니다.'}
    ]
)

final_response = response.choices[0].message.content
print(final_response)