import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DB_DIR = "./chroma_db"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


def build_collection(
    txt_path,
    collection_name,
    chunk_size=500,
    chunk_overlap=100
):
    """
    txt 파일을 읽어서
    Collection 생성
    """

    # txt 읽기
    docs = TextLoader(
        txt_path,
        encoding="utf-8"
    ).load()

    # metadata 추가
    for doc in docs:
        doc.metadata["source"] = collection_name

    # 청킹
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_documents(docs)

    # Collection 생성
    store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=DB_DIR
    )

    print(
        f"{collection_name} 생성 완료 "
        f"({len(chunks)} chunks)"
    )

    return store


# 생성할 Collection 목록
FILES = {
    "hbm": "./hbm.txt",
    "nvme": "./nvme.txt"
}

for collection_name, path in FILES.items():

    build_collection(
        txt_path=path,
        collection_name=collection_name
    )