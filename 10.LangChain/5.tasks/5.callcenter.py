# 목적 - 질문 유형에 따라 적합한 항목으로 답변한다.
# 질문 유형 -> 배송조회 상담원
#          -> 결제관련 상담원
#          -> 기술지원 상담원
# RunnableBranch

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser
from langchain_core.runnables import RunnableBranch

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

def make_chain(role):
    return(
        ChatPromptTemplate.from_messages([
            ('system', role),
            ('user', "{question}")
        ])
        | llm
        | StrOutputParser()
    )

# 개발자냐/요리사냐/일반
delivery_chain = make_chain("당신은 배송조회 상담원입니다.")
charge_chain = make_chain("당신은 결제관련 상담원입니다.")
tech_chain = make_chain("당신은 기술지원 상담원입니다.")
default_chain = make_chain("당신은 일반 상담원입니다.")

branch = RunnableBranch(
    (
        lambda x: "배송" in x['question'] or '택배' in x['question'],
        delivery_chain
    ),
    (
        lambda x: "결제" in x['question'] or '환불' in x['question'],
        charge_chain
    ),
    (
        lambda x: "전산" in x['question'] or '오류' in x['question'],
        tech_chain
    ),
    default_chain
)

questions = [
    "택배 언제와",
    "결제 잘못했어",
    "결제 오류났어"
]

for q in questions:
    print('질문: ', q)
    print('답변: ', branch.invoke({'question': q}))
    print('-'*60)