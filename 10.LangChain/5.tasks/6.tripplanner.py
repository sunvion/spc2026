# 목적 - 여행 계획을 작성한다.
# 도시 입력 -> 음식 추천
#          -> 관광지 추천
#          -> 호텔 추천
# 사용자의 입력 OO을 보고, 시간표/동선/교통수단 vs 음식/관광지/호텔
# RunnableParallel, RunnableBranch

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda

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
cook_chain = (
    RunnableLambda(lambda x: print(">>> 음식 추천 실행") or x)
    | make_chain("당신은 여행사의 음식 부분 기획 담당자입니다.")
)
tour_chain = (
    RunnableLambda(lambda x: print(">>> 관광지 추천 실행") or x)
    | make_chain("당신은 여행사의 관광 부분 기획 담당자입니다.")
)
hotel_chain = (
    RunnableLambda(lambda x: print(">>> 호텔 추천 실행") or x)
    | make_chain("당신은 여행사의 숙소 기획 담당자입니다.")
)
general_chain = (
    RunnableLambda(lambda x: print(">>> 여행 추천 실행") or x)
    | make_chain("당신은 배낭 여행자입니다.")
)

branch = RunnableBranch(
    (
        lambda x: "음식" in x['question'] or '식당' in x['question'] or '음료' in x['question'],
        cook_chain
    ),
    (
        lambda x: "관광지" in x['question'] or '명소' in x['question'] or '볼만한' in x['question'],
        tour_chain
    ),
    (
        lambda x: "숙소" in x['question'] or '숙박' in x['question'] or '화장실' in x['question'] or '벌레' in x['question'],
        hotel_chain
    ),
    general_chain
)

questions = [
    "태국 방콕 식당 추천해줘.",
    "서울에서 구경하기 좋은 곳 알려줘",
    "중국 베이지의 깨끗한 화장실이 있는 숙소 찾아줘.",
    "여행 가고 싶어. 추천해줘."
]

for q in questions:
    print('질문: ', q)
    print('답변: ', branch.invoke({'question': q}))
    print('-'*60)