import os
from dotenv import load_dotenv

from openai import OpenAI

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

client = OpenAI()

DB_DIR = "./chroma_db"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# -------------------------
# Collection 로드
# -------------------------

hbm_store = Chroma(
    collection_name="hbm",
    embedding_function=embeddings,
    persist_directory=DB_DIR
)

nvme_store = Chroma(
    collection_name="nvme",
    embedding_function=embeddings,
    persist_directory=DB_DIR
)

# -------------------------
# 사용자 질문
# -------------------------

question = "HBM과 NVMe의 차이점을 비교해줘"

# -------------------------
# 각각 검색
# -------------------------

hbm_docs = hbm_store.similarity_search(
    question,
    k=3
)

nvme_docs = nvme_store.similarity_search(
    question,
    k=3
)

# -------------------------
# 검색 결과 합치기
# -------------------------

hbm_text = "\n\n".join(
    doc.page_content
    for doc in hbm_docs
)

nvme_text = "\n\n".join(
    doc.page_content
    for doc in nvme_docs
)

context = f"""
[HBM 문서]

{hbm_text}

[NVMe 문서]

{nvme_text}
"""

# -------------------------
# GPT에게 전달
# -------------------------

prompt = f"""
다음 자료를 참고해서 답변해라.

{context}

질문:
{question}

다음 형식으로 답변해라.

1. 정의
2. 구조
3. 성능
4. 장점
5. 단점

표 형태로 비교해라.
"""

response = client.responses.create(
    model="gpt-5",
    input=prompt
)

print(response.output_text)