from dotenv import load_dotenv
import os
import requests

load_dotenv()

open_api_key = os.getenv('OPENAI_API_KEY')
user_input = '강아지를 데려올 건데, 이름 후보군을 알려줘.'

response = requests.post(
    'https://api.openai.com/v1/chat/completions',
    json={
        'model': 'gpt-3.5-turbo',
        'messages': [
            # {'role': 'system', 'content': 'You are a helpful assistant'},
            # {'role': 'system', 'content': '너는 나를 잘 도와주는 사람이야.'},
            # {'role': 'system', 'content': '너는 나를 잘 도와주는 경력 20년차의 개발자야.'},
            {'role': 'system', 'content': '너는 나를 잘 도와주는 경력 20년차의 작명가야.'},
            {'role': 'user', 'content': user_input}
        ],
        'temperature': 1.3
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {open_api_key}" # Basic 인증 = Basic Authorization
    }
)

data = response.json()
final_response = data['choices'][0]['message']['content']
print(final_response)