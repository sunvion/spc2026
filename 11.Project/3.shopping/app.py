import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

from flask import Flask, send_from_directory, jsonify, request

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
app = Flask(__name__, static_folder='public')

reviews =[] # 사용자들의 댓글을 저장할 변수 (평점과 후기가 함께 들어간다. {'rating': 값, 'comment': 값})

# ---------------
# API 라우팅
# ---------------
@app.route('/api/reviews', methods = ['POST']) # POST로 받기
def add_review():
    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment')
    # reviews에 저장하기
    reviews.append({'rating': rating, 'comment': comment})
    return jsonify({'message': '리뷰 저장 완료'})

@app.route('/api/reviews', methods = ['GET']) # GET으로 받기
def get_review():
    # reviews를 가져와서 반환하기
    review_text = ''
    for review in reviews:
        review_text += f"{review['rating']}점 - {review['comment']}\n"
    return jsonify(review_text)

@app.route('/api/ai-summary', methods = ['GET']) # GET으로 받기
def get_ai_summary():
    # reviews를 가져와서
    review_text = ''
    for review in reviews:
        review_text += f"{review['rating']}점 - {review['comment']}\n"
    if len(reviews) > 0:
        total_rating += int(review['rating'])
        average_rating = total_rating / len(reviews)
    else :
        average_rating = 0
    # 여기에서 프롬프트 및 api 호출 코드 작성
    prompt = f"""
아래 리뷰들을 요약해줘

{review_text}
"""
    print("작성된 리뷰 내용: ", prompt)

    # chatgpt API로 요청한다.
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {'role': 'system', 'content': '당신은 리뷰를 분석하는 담당자입니다.'},
            {'role': 'user', 'content': prompt}
        ]
    )
    chatbot_reply = response.choices[0].message.content

    # 응답을 받아와서 변환한다.
    return jsonify({'summary': chatbot_reply, 'average_rating': average_rating})

# ---------------
# 웹서비스 라우팅
# ---------------
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)

