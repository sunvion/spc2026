from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

loader = PyPDFLoader("./Javascript_Secure_Coding.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

store = Chroma.from_documents(
    chunks,
    embeddings,
    collection_name="pdf_docs",
    persist_directory="./chroma_db"
)

print("저장 완료")

store = Chroma(
    collection_name="pdf_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

results = store.similarity_search(
    "JavaScript 코드를 짤 때의 보안 대전제는?",
    k=3
)

for doc in results:
    print(doc.page_content)