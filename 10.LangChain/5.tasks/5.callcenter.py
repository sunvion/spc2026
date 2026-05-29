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

# ======================= 강사님 답안 =============================
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

payment_chain = make_chain("당신은 결제 상담원입니다. 결제/환불/청구 문제에 대해 친절하게 안내하세요.")
delivery_chain = make_chain("당신은 배송 상담원입니다. 배송 조회/지연/반품 문제에 대해 친절하게 안내하세요.")
tech_chain = make_chain("당신은 기술 지원 상담원입니다. 웹/서비스/제품설명 등 사용법과 오류를 해결하는 단계를 친절하게 안내하세요.")
general_chain = make_chain("당신은 일반 고객 상담원입니다. 친절하고 간략하게 답변하세요.")

branch = RunnableBranch(
    (lambda x : any(k in x["question"] for k in ["결제", "환불", "청구"]), payment_chain),
    (lambda x : any(k in x["question"] for k in ["배송", "택배", "반품"]), delivery_chain),
    (lambda x : any(k in x["question"] for k in ["오류", "에러", "안돼요"]), tech_chain),
    general_chain, # 위에가 다 매칭이 안되면 최종적으로 연결.
)

questions = [
    "택배 언제와",
    "결제 잘못했어",
    "결제 오류났어"
]

for q in questions:
    print('-'*60)
    print(f'고객: ', q)
    print(f'상담원: ', branch.invoke({'question': q}))
