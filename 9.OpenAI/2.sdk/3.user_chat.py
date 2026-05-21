# pip uninstall openai; pip install openai # 현재 최신은 4.x
import openai

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')

openai_api_key = os.getenv('OPENAI_API_KEY')

client = openai.OpenAI(api_key=openai_api_key)

def ask_chatbot(user_input):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages = [
            {'role': 'system', 'content':'당신은 나의 질문에 대답을 잘하는 쳇봇입니다.'},
            {'role': 'user', 'content':user_input}
        ]
    )

    final_response = response.choices[0].message.content
    return final_response

while True:
    user_input = input('\n질문: ').strip()
    chatbot_response = ask_chatbot(user_input)
    print('챗봇 응답: ', chatbot_response)