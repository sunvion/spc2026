from dotenv import load_dotenv
import os
import requests

load_dotenv()

open_api_key = os.getenv('OPENAI_API_KEY')

# 대화 히스토리
message = [
    {'role': 'system', 'content': '너는 나를 잘 도와주는 경력 20년차의 작명가야.'}
]


def call_gpt(messages, temperature=1.0):
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        json={
            'model': 'gpt-3.5-turbo',
            'messages': messages,
            'temperature': temperature
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {open_api_key}"
        }
    )
    data = response.json()
    return data['choices'][0]['message']['content']


def summarize_recent(messages):
    """
    최근 대화 10개를 압축 요약
    """
    recent = messages[1:][-10:]  # system 제외 + 최근 10개

    if len(recent) == 0:
        return None

    summary_prompt = [
        {
            "role": "system",
            "content": "너는 대화를 매우 짧게 압축 요약하는 AI야. 핵심만 3~5줄 bullet로 정리해."
        }
    ] + recent

    return call_gpt(summary_prompt, temperature=0.2)


def compress_memory():
    """
    최근 10개 대화를 요약해서 system memory로 압축
    """
    global message

    summary = summarize_recent(message)
    if not summary:
        return

    # 압축된 기억을 system 메모리에 추가
    message = [
        message[0],
        {
            "role": "system",
            "content": f"[이전 대화 요약]\n{summary}"
        }
    ] + message[-6:]  # 최근 일부만 유지


def ask_chatbot(user_input):
    try:
        global message

        message.append({'role': 'user', 'content': user_input})

        reply = call_gpt(message, temperature=1.3)

        message.append({'role': 'assistant', 'content': reply})

        # 🔥 핵심: 일정 길이 넘으면 자동 압축
        if len(message) > 12:  # system + summary + 최근 메시지 초과 시
            compress_memory()

        return reply

    except Exception as e:
        print('오류:', e)
        return '오류가 발생했습니다.'


# =========================
# 챗봇 실행 루프
# =========================

while True:
    user_input = input('\n당신의 질문: ').strip()

    if user_input.lower() in ['quit', 'exit', '종료', '끝']:
        print('\n대화를 종료합니다. 최종 요약 생성 중...\n')

        final_summary = summarize_recent(message)

        print('\n📌 최종 대화 요약')
        print('-' * 60)
        print(final_summary)
        print('-' * 60)

        print('안녕히 계세요')
        break

    print('대화를 생성중입니다. 잠시만 기다려 주세요...')
    print('챗봇 응답:', ask_chatbot(user_input))
    print('-' * 60)