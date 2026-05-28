# pip install langchain langchain-openai

import os
from dotenv import load_dotenv

# from langahin.llms import OpenAI # 구버전
from langchain_openai import OpenAI # 신버전

load_dotenv()
openai_api_key = os.getenv('OPENATI_API_KEY')

# llm = OpenAI(model = 'gpt-4o-mini') # 기본 환경변수 키
llm = OpenAI(model = 'gpt-4o-mini')
# llm = OpenAI(model = 'gpt-4o-mini', openai_api_key=openai_api_key)
# llm = OpenAI(model = 'gpt-4o-mini', api_key=openai_api_key)
# print(llm)

prompt = "오늘 저녁은 무엇을 먹을까요?"
result = llm.invoke(prompt)
print(result)