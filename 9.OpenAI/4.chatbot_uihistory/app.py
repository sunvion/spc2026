from flask import Flask, request, jsonify, send_from_directory
import openai
import os, requests
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__, static_folder='static', static_url_path='') # static 폴더 경로와 그 prefix를 결정(변경)할 수 있음

history = []

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    chat_message = data.get('chatMessage', '')
    print("사용자 입력값: ", chat_message)

    # ChatGPT 응답 받기
    get_reply = ask_chatgpt(chat_message)

    # JSON 형태로 반환
    return jsonify({'reply': get_reply})

def ask_chatgpt(chat_message):

    gpt_ask_message = [
        {'role': 'system', 'content': '당신은 친절한 챗봇입니다. 경상도 사투리 사용'}*history
    ]

    print = ('>>>>>>>>>>')
    print = ('최종 GPT에게 우리가 물어볼 전체 메시지: ', )
    print = ('<<<<<<<<<<')
    response = client.chat.completions.create(
        model = 'gpt-4o-mini', # 웬만한 우리 실습은 gpt-4o-mini
        messages = [
            {'role': 'system', 'content': '당신은 친절한 챗봇입니다.'},
            {'role': 'user', 'content': chat_message}
        ]
    )
    print('출력확인: ', response)
    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)