# 1. openai 관련 라이브러리를 다 불러온다 (dotenv, openai 등등)
# 2. OOO 페이지 (우리의 최종 페이지) 에서 채팅창 FE 를 만든다.
# 3-1. 그 FORM의 입력값을 BE에서 POST로 받아서, chatgpt API 호출한다. (그냥 아무말이나 해도 됨.)
# 3-2. 응답 받아서 다시 프런트엔드에 반환해서 결과 출력한다. 
# 3-3. [추가] 복습을 원하면 SSE 기반에 스트리밍 구현해봐도 됨
# 4. 그럼 이제, 진짜 우리의 이 상황 (학년, 커리큐럼) 에 대해서 영어로 대화를 하도록 만든다.
# 5. [추가] 메모리를 통해서 대화 내용 컨텍스트를 기억하게 한다.

# 환경 변수 불러온다.
import os
from dotenv import load_dotenv

# OpenAI 라이브러리
from openai import OpenAI

# 웹서비스 기본 프레임워크
from flask import Flask, render_template, request, jsonify

load_dotenv()

openai_api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
app = Flask(__name__)

# 각 학년별 커리큐럼 데이터
curriculums = {
    # key: [values]
    1: ['기초 인사', '간단한 문장', '동물 이름'],
    2: ['학교 생활', '가족 소개', '자기 소개'],
    3: ['취미와 운동', '날씨 묘사', '간단한 이야기'], # 나중에 내용을 바꾸거나 목록을 추가하거나 해볼 것
    4: ['쇼핑과 가격', '음식 주문', '여행 이야기'],
    5: ['역사와 문화', '과학과 자연', '사회 이슈'],
    6: ['미래 계획', '진로 탐색', '세계 여행'],
}

@app.route('/')
def home():
    return render_template('home.html', grades=curriculums.keys())

@app.route('/grade/<int:grade>')
def grade(grade):
    if grade in curriculums:
        curriculums_index = list(enumerate(curriculums[grade]))
        return render_template('grade.html', grade=grade, grades=curriculums.keys(), curriculums=curriculums_index)
    return "해당 학년은 존재하지 않습니다.", 404

@app.route('/grade/<int:grade>/curriculum/<int:curriculum_id>', methods=['GET', 'POST'])
def curriculum(grade, curriculum_id):
    if grade in curriculums and 0 <= curriculum_id < len(curriculums[grade]):
        curriculum_title = curriculums[grade][curriculum_id]

        # POST 처리하는 곳
        if request.method == 'POST':
            user_input = request.form.get('user_input')
            print(f"학년: {grade}, 커리큐럼: {curriculum_title}, 사용자입력: {user_input}")

            # 실무적으로는 이런 프롬프트 스테이트먼트를 별도 파일로 분리하는 것이 더 좋음.
            system_prompt = f"""
You are a friendly English teacher for grade {grade} students.

Topic: {curriculum_title}

RULES:
- The student may speak in Korean or English.
- Always respond mainly in English.
- If needed, add short Korean explanations in parentheses.
- Encourage the student to speak more English.
- Never write dialogue format (no "Student:" or "Teacher:").
- Keep answers simple and short (1–3 sentences).
- If the student uses Korean, translate it naturally into English and continue the conversation.
"""
            user_prompt = f"학생이 영어로 질문하면 영어로 답변하고, 한국말로 질문하면 한국말과 영어를 적절하게 섞어서 답변을 하며, 영어를 사용하도록 유도해야 합니다. 학생이 다음과 같이 질문합니다. :\n{user_input}"

            print('우리가 GPT에게 던질 질문 SP: ', system_prompt)
            print('우리가 GPT에게 던질 질문 UP: ', user_prompt)

            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    # 나는 여기 뭐라고 입력해야 그 사용자의 상황에 맞는 질문을 할 것이냐? < 프롬프트 엔지니어링
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
            )
            chat_reply = response.choices[0].message.content
            return jsonify({'response' : chat_reply})

        # GET 처리하는 곳
        return render_template('curriculum.html', grade=grade, grades=curriculums.keys(), curriculum_title= curriculum_title)
    
    # 입력값에 오류가 있는 경우
    return "해당 커리큘럼은 존재하지 않습니다.", 404

# @app.route('/api/chat', methods=['POST'])
# def chat():
#     user_input = request.form.get('user_input')
#     print('사용자입력: ', user_input) 
# 분리해서 작성하는 방법

if __name__ == "__main__":
    app.run(debug=True)