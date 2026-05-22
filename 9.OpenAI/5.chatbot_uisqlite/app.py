from flask import Flask, request, jsonify, send_from_directory
import openai
import os, requests, sqlite3
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__, static_folder='static', static_url_path='') # static 폴더 경로와 그 prefix를 결정(변경)할 수 있음

# history = []  이것을 대체할 DB 코드를 넣기
conn = sqlite3.connect('chatgpt.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
    conn.commit()
init_db()

def save_message(role, content):
    
    conn.commit()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    chat_message = data.get('chatMessage', '')
    print("사용자 입력값: ", chat_message)

    # SQL INSERT 구문 넣기
    cursor.execute("INSERT INTO history (role, content) VALUES (?, ?)",('user', chat_message))

    # ChatGPT 응답 받기
    get_reply = ask_chatgpt(chat_message)

    cursor.execute("INSERT INTO history (role, content) VALUES (?, ?)",('user', chat_message))

    # JSON 형태로 반환
    return jsonify({'reply': get_reply})

def ask_chatgpt(chat_message):

    cursor.execute("SELECT role, content FROM history ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    print(rows)
    rows = rows[::-1] # 역순으로 다시 배열 넣기
    print('역순 재변환: ', rows)

    row_dict = [{'role': row['role'], 'content': row['content']} for row in rows]
    print('-'*30)
    print(row_dict)

    gpt_ask_message = [
        {'role': 'system', 'content': '당신은 친절한 챗봇입니다. 경상도 사투리를 적절하게 섞어서 답변하시오'}
        {'role': 'user', 'content': chat_message}
    ]

    print = ('>>>>>>>>>>')
    print = ('최종 GPT에게 우리가 물어볼 전체 메시지: ', )
    print = ('<<<<<<<<<<')
    response = client.chat.completions.create(
        model = 'gpt-4o-mini', # 웬만한 우리 실습은 gpt-4o-mini
        messages = chat_message
    )
    print('출력확인: ', response)
    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)