# pip install chromadb
# pip install langchain-chroma
# pip install langchain-openai
# pip install python-dotenv

from dotenv import load_dotenv

from langchain_openai import (
    OpenAIEmbeddings,
    ChatOpenAI
)

from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

DB_DIR = "./chroma_db"

# 임베딩 모델
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# 기존 DB 로딩
store = Chroma(
    collection_name="hbm",
    embedding_function=embeddings,
    persist_directory=DB_DIR
)

# Retriever 생성
retriever = store.as_retriever(
    search_kwargs={"k": 3}
)

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini"
)

# Prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
당신은 문서 기반 Q&A 시스템입니다.

반드시 제공된 문서만 참고해서 답변하세요.

문서에 없는 내용은
'문서에서 찾을 수 없습니다.'
라고 답변하세요.

문서:
{context}
"""
    ),
    ("user", "{question}")
])

# 질문
question = "HBM과 NVMe의 차이점은 무엇인가요?"

# chain 실행
def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

docs = retriever.invoke(question)

print("===== 검색 문서 =====")
for i, d in enumerate(docs, 1):
    print(f"{i}. {d.page_content}")

answer = chain.invoke(question)

print("\n===== 답변 =====")
print(answer)