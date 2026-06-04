import os
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, send_from_directory, jsonify, request

load_dotenv()

openai_api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
app = Flask(__name__, static_folder='public')

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/codecheck', methods=['POST'])
def code_check():
    # 데이터를 JSON 형태로 받아온다.
    # 프론트에서 보낸 데이터 받기
    data = request.get_json()
    user_input = data.get('user_input')

    # system prompt
    system_prompt = """
너는 전문 코드 분석 및 디버깅 AI이다.

사용자가 작성한 코드를 분석하여 다음 작업을 수행한다.

1. 코드 오류 분석
- 발생 가능한 에러를 찾는다.
- 에러 원인을 설명한다.
- 해결 방법을 제시한다.

2. 코드 디버깅
- 잘못된 문법이나 로직을 수정한다.
- 수정된 코드 예시를 제공한다.

3. 보안 취약점 분석
- SQL Injection
- XSS
- 인증 및 권한 문제
- 하드코딩된 민감 정보
- 위험한 입력 처리
등의 취약점을 탐지한다.

4. 코드 개선
- 더 효율적인 코드 구조를 제안한다.
- 가독성을 높이는 방법을 설명한다.

응답 규칙:
- 초보 개발자도 이해할 수 있게 쉽게 설명한다.
- 필요한 경우 단계별로 설명한다.
- 코드 예시는 가능한 한 완전한 형태로 제공한다.
- 답변은 한국어 중심으로 작성한다.
- 프로그래밍 용어와 코드 키워드는 영어 그대로 사용한다.
"""

    # user prompt
    user_prompt = f"""
사용자가 다음 코드를 분석해달라고 요청했습니다.

[사용자 입력 코드]
{user_input}

다음을 수행하세요:
1. 코드 오류 분석
2. 보안 취약점 검사
3. 문제 원인 설명
4. 수정 방법 제안
5. 필요하면 수정된 코드 제공
"""

    print('응답:', system_prompt)
    print('유저 질문:', user_prompt)

    # ChatGPT API 요청
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    # 응답 내용 추출
    result = response.choices[0].message.content

    # 응답을 받아와서 변환한다.
    return jsonify({
        'result': result
    })

if __name__ == '__main__':
    app.run(debug=True)