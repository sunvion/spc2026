# 목적 - 뉴스 입력 -> 요약
#                -> 감정분석
#                -> 카테고리 분석
# RunnableParallel

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

summary_prompt = ChatPromptTemplate.from_messages([
    ('system', "당신은 뉴스 요약 전문가입니다. 다음 뉴스를 3줄로 요약하세요."),
    ('user', "{article}")
])

emotion_prompt = ChatPromptTemplate.from_messages([
    ('system', "다음 뉴스 기사의 감정을 분석하여 [긍정, 중립, 부정] 중 하나로 답변하고 이유를 쓰세요."),
    ('user', "{article}")
])

category_prompt = ChatPromptTemplate.from_messages([
    ('system', "다음 뉴스 기사의 카테고리(정치, 경제, 사회, IT/과학 등)를 분류하세요."),
    ('user', "{article}")
])

summary_chain = (
    summary_prompt
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

emotion_chain = (
    emotion_prompt
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

category_chain = (
    category_prompt
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

parallel_chain = RunnableParallel({
    "summary": summary_chain,
    "emotion": emotion_chain,
    "category": category_chain,
})

result = parallel_chain.invoke({
    "article": """
국내 증시의 ‘큰손’인 국민연금이 올해 국내 주식투자 목표 비중을 기존 14.9%에서 20.8%로 올려 잡았다. 이 목표치보다 폭넓은 운용을 가능하게 하는 전략적 자산배분 허용 범위도 한시적으로 기존 ±5%포인트에서 ±10%포인트로 넓혔다. 이렇게 되면 국민연금이 담을 수 있는 국내 주식 비중이 최대 30% 수준으로 늘어난다. 기존 한도를 유지하면 최대 170조원어치 국내 주식을 팔아야 한다는 부담 등을 고려해 보유 한도를 높였다.

국민연금기금운용위원회는 28일 정부서울청사에서 올해 제5차 회의를 열고 국내 주식투자 비중을 20.8%로 5.9%포인트 상향하는 내용이 담긴 ‘2027~2031년 중기자산 배분안’을 심의·의결했다. 지난해 5월 의결한 배분안에선 국민연금의 올해 국내 주식 목표 비중은 14.4%였다. 올해 1월 기금위는 이를 14.9%로 늘렸다. 중기자산 배분은 앞으로 5년간 기금 목표 수익률과 자산군별 목표 비중을 정하는 국민연금 기금 운용의 핵심 계획이다.

국민연금은 기금의 장기 수익성과 안정성을 높이기 위해 자산군이나 지역(국내·해외)별로 투자 비율을 정해 위험을 분산한다. 이번 배분안은 2027년부터 적용되지만, 코스피 급등으로 국내 주식 비중이 이미 허용 범위를 넘어서자 기금위가 미리 나섰다. 반도체주를 중심으로 한 주가 급등으로 국민연금의 국내 주식 비중은 지난 2월 기준 24.5%까지 상승했다. 이는 국민연금이 지난 1월 14.4%에서 상향 조정한 목표 비중(14.9%)과 최대 허용치(19.9%)를 모두 웃돈다.

기금위가 비중을 상향한 이유는 시장 충격 우려 때문이다. 국내 증시 최대 기관투자자인 국민연금은 삼성전자 지분 7.8%, SK하이닉스 지분 8.1%를 보유하고 있다. 두 종목 평가액만 이날 기준 269조원에 이른다. 목표 비중을 맞추려고 대규모 매도에 나선다면 국내 증시에 미치는 충격이 상당할 것이란 지적이 있었다.

국민연금은 2021년 이른바 ‘코로나19 불장’ 때 코스피가 처음으로 3000선을 돌파하자 자산배분 원칙에 따라 51거래일 연속 순매도에 나섰다가 “국민 염원에 찬물을 끼얹는 행위”(청와대 국민청원)라는 비판에 휩싸이기도 했다. 기금위는 일본의 사례를 참고한 것으로 전해진다. 2014년 일본 공적연금(GPIF)은 자국 주식 목표 비중을 12%에서 25%로 대폭 확대했다. 당시 아베노믹스의 중요한 축 중 하나인 증시 활성화 유도 조치였다.

국내 주식 목표 비중 20.8%에, 전략적 자산배분(SAA)과 전술적 자산배분(TAA) 허용 범위(±10%포인트)까지 포함하면 최대치는 30%가량이 된다. 기금 규모를 1800조원으로 봤을 때 국내 주식 보유 가능액은 약 370조원에서 약 540조원까지 불어난다. 국민연금으로선 이번 조치로 최대 170조원 상당 국내 주식을 팔아야 하는 부담을 벗었다는 의미다.

급한 불을 껐지만 우려도 작지 않다. 익명을 요구한 증권업계 관계자는 “언젠가는 국내 주식을 본격적으로 팔아야 하는 시기가 올 텐데 그런 상황에 대비해 자산을 다변화하고 원칙에 따라 운용해야 한다”고 강조했다. 연금연구회는 28일 성명서를 내고 “향후 국내 증시가 조정을 받을 경우 그 손실은 고스란히 미래 연금 수급세대가 떠안을 수밖에 없다”고 했다. 윤석명 한국보건사회연구원 명예연구위원은 “전 세계 주요 연기금의 경우 정치적 간섭에서 벗어나려 해외 투자의 중요성을 강조하는데 우리만 거꾸로 가는 것”이라고 말했다.
"""
})

print(result)