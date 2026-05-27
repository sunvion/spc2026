import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

from flask import Flask, send_from_directory, jsonify, request

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
app = Flask(__name__, static_folder='public')

@app.route('/')
def index():
    return send_from_directory('public', 'index_plus.html')

@app.route('/api/codecheck', methods=['POST'])
def code_check():
    # 데이터를 JSON 형태로 받아온다.
    data = request.get_json()
    url = data.get('code')
    url_plus = (url.replace('github', 'raw.githubusercontent', 1)
                .replace('/blob/', '/', 1))
    print(url_plus)
    
    info = data.get('info')
    sqli = data.get('sqli')
    xss = data.get('xss')

    response = requests.get(url_plus)
    source_code = response.text

    prompt = (
        "다음 소스코드를 보고 취약점을 분석하세요.\n"
    )

    if info:
        prompt += "하드코딩된 비밀번호, API KEY 같은 민감정보가 있는지도 확인하세요.\n"

    if sqli:
        prompt += "SQL Injection 취약점 여부를 중점적으로 분석하세요.\n"

    if xss:
        prompt += "XSS 취약점 여부를 중점적으로 분석하세요.\n"

    prompt += (
        "\n각 취약점에 대해 해당 코드의 라인 번호, 코드 스니펫, "
        "취약점 설명과 개선 방안을 간단하게 설명하시오.\n\n"
        "소스코드:\n"
        "----------\n"
        f"{source_code}\n"
        "----------\n"
    )
    print("실제로 우리가 질문할 내용: ", prompt)

    # chatgpt API로 요청한다.
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {'role': 'system', 'content': '당신은 소스코드 분석 보안 전문가입니다.'},
            {'role': 'user', 'content': prompt}
        ]
    )
    chatbot_reply = response.choices[0].message.content

    # 응답을 받아와서 변환한다.
    return jsonify({'result': chatbot_reply})

if __name__ == '__main__':
    app.run(debug=True)