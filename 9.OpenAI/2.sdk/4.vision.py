# pip uninstall openai; pip install openai # 현재 최신은 4.x
import openai

from dotenv import load_dotenv
import os, base64

load_dotenv(dotenv_path='../.env')

openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=openai_api_key)

# 이런 변환함수를 일일이 다 암기할 필요는 없음, 하지만 인코딩이 뭔지 왜 해야하는지 알아야함.
def encode_image_to_base64(image_path):
    # 이미지를 읽어서 base64로 인코딩하는 함수 구현
    with open(image_path, 'rb') as file:
        base64_str = base64.b64encode(file.read()).decode("utf-8")
        return base64_str


# 이미지 + 질문 보내기
def ask_chatbot(image_path, user_input):
    image_base64 = encode_image_to_base64(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "당신은 이미지를 보고 분석하는 AI입니다."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_input},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

while True:
    user_input = input('\n질문: ').strip()
    chatbot_response = ask_chatbot(user_input)
    print('챗봇 응답: ', chatbot_response)