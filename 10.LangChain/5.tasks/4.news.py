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

base_prompt = ChatPromptTemplate.from_messages([
    ('system', "다음 뉴스를 요약하고 {emotion} 분석과 {category}를 분류하시오."),
    ('user', "{article}")
])

score_5 = (
    base_prompt.partial(emotion="긍정")
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

score_3 = (
    base_prompt.partial(emotion="중립")
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

score_1 = (
    base_prompt.partial(emotion="부정")
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

category = (
    base_prompt.partial(category="뉴스 기사 주제")
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

parallel_chain = RunnableParallel({
    "english": chain_en,
    "chinese": chain_ch,
    "japenese": chain_ja,
    "franch": chain_fr,
})

result = parallel_chain.invoke({
    "text": "안녕하세요, 만나서 반갑습니다."
})

print(result)

# ==========
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnableParallel

# load_dotenv()

# llm = ChatOpenAI(model="gpt-4o-mini")

# # 1. 각 목적에 맞는 프롬프트 분리 구성 (이 방식이 훨씬 직관적이고 에러가 적습니다)
# summary_prompt = ChatPromptTemplate.from_messages([
#     ('system', "당신은 뉴스 요약 전문가입니다. 다음 뉴스를 3줄로 요약하세요."),
#     ('user', "{article}")
# ])

# emotion_prompt = ChatPromptTemplate.from_messages([
#     ('system', "다음 뉴스 기사의 감정을 분석하여 [긍정, 중립, 부정] 중 하나로 답변하고 이유를 쓰세요."),
#     ('user', "{article}")
# ])

# category_prompt = ChatPromptTemplate.from_messages([
#     ('system', "다음 뉴스 기사의 카테고리(정치, 경제, 사회, IT/과학 등)를 분류하세요."),
#     ('user', "{article}")
# ])

# # 2. 개별 체인 생성 (StrOutputParser를 쓰면 content.strip()을 알아서 해줍니다)
# summary_chain = summary_prompt | llm | StrOutputParser()
# emotion_chain = emotion_prompt | llm | StrOutputParser()
# category_chain = category_prompt | llm | StrOutputParser()

# # 3. RunnableParallel 구성 (위에서 만든 체인들을 매핑)
# parallel_chain = RunnableParallel({
#     "요약": summary_chain,
#     "감정분석": emotion_chain,
#     "카테고리": category_chain
# })

# # 4. 실제 뉴스 기사 입력 및 실행
# news_article = """
# 정부가 AI 반도체 산업 육성을 위해 2026년까지 총 5조 원 규모의 예산을 투입하기로 결정했습니다. 
# 이번 투자를 통해 글로벌 시장에서의 기술 주도권을 선점하고 국내 스타트업들의 성장을 적극 지원할 방침입니다. 
# 업계 관계자들은 이번 발표에 대해 환영의 뜻을 밝히며, 내수 활성화에도 큰 도움이 될 것으로 기대하고 있습니다.
# """

# # 입력 키는 프롬프트에서 선언한 {article}과 일치해야 합니다.
# result = parallel_chain.invoke({
#     "article": news_article
# })

# # 5. 결과 출력
# import json
# print(json.dumps(result, ensure_ascii=False, indent=2))