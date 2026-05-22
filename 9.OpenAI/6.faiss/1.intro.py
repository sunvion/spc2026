# pip install faiss-cpu

from dotenv import load_dotenv
import os

from openai import OpenAI

import faiss
import numpy as np

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 우리의 문장 데이터
documents = [
    '한국소프트웨어저작권협회는 SPC라는 약자를 가지고 있고, 다양한 국내 기업의 SW라이선스와 저작권을 다루는 곳입니다.',
    '홍길동은 2020년 1월 1일 생으로, 강원도 설빙산에서 태어났고, 그곳에서 호랑이를 잡아먹으며 성장하였습니다.',
    'Python은 개발 언어 중에 가장 쉽다고 하는데, 그렇게 쉬운 언어는 아닙니다.'
]

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model='text-embedding-ada-002'
    )
    # print(response)
    return np.array(response.data[0].embedding)

# print(get_embedding(documents))
index = faiss.IndexFlatL2(1536) # OpenAI로 임베딩하면 1536 차원
doc_embeddings = np.array([get_embedding(doc) for doc in documents])
index.add(doc_embeddings) # 나온 숫자값을 백터DB에 넣는다.

# 사용자의 질문을 받아서 우리의 백터DB에 물어본다
def rag_query(user_query):
    query_embedding = get_embedding(user_query)
    print(query_embedding)
    _, indices = index.search(np.array([query_embedding]), k=1) # 백터DB에서 (user_query)의 숫자값과 가장 가까운 k=1 개를 반환하시오.
    retrieved_doc = documents[indices[0][0]]

    prompt = f"""
    아래 내용을 보고 답변하시오. 아래 질문과 관련자료가 연관이 없거나, 답변을 할 수 없는 내용이면, 적절한 미사여구를 그때그때 다르게 붙여서 답변을 할 수 없다고 하시오.

    사용자의 질문: {user_query}

    관련자료: {retrieved_doc}
    """

    print(">>>>>")
    print("우리가 실제로 gpt에게 물어보는 내용\n", prompt)
    print("<<<<<")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 친절한 AI도우미 입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
    # print(indices)
    # print(retrieved_doc)
    # return retrieved_doc

query = '홍길동은 누구인가요?'
# query = '저작권협회는 누구인가요?'
# query = '파이썬은 어떤 언어인가요?'
# query = '오늘 저녁은 뭐 먹을까?'

print(rag_query(query))