# 목적: 긴 문장을 받아서 짧게 요약한다.

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate
)
from langchain_core.runnables import RunnableLambda

load_dotenv()

template = "다음의 긴 내용을 3개의 문장으로 요약하시오:\n\n{article}"
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template('당신은 전문 문장 요약가입니다.'),
    HumanMessagePromptTemplate.from_template(template)
])

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.3) # 이런 경우는 0.3~0.5

chain = chat_prompt | llm | RunnableLambda(lambda x: {'summary': x.content.strip()})

input_text = {
    "article": "한은이 사실상 금리 인상 사이클 진입을 예고하면서 대출자들의 발등에도 불이 떨어졌다. 금리 인상 시점과 폭에 대한 전망이 앞당겨지자 시장금리도 선제적으로 움직이고 있기 때문이다. 실제 서울 채권시장에서 국고채 3년물 금리는 이날 한때 연 3.808%까지 치솟았다. 전날 3.711%와 비교하면 하루 만에 0.097%포인트 오른 수준이다. 국고채 금리는 은행 조달금리의 방향을 보여주는 대표 시장금리로 상승세가 이어질 경우 주택담보대출과 신용대출 금리에도 시차를 두고 반영될 가능성이 크다."
"금리 상승은 가계부채 부담으로 이어질 수 있다. 한은에 따르면 올해 3월 말 기준 가계신용 잔액은 1993조1000억원으로 집계됐다. 지난해 말보다 14조원 늘어난 규모다. 금융위원회가 집계한 4월 말 기준 금융권 주택담보대출도 5조5000억원 증가해 전월 증가폭인 3조원을 웃돌았다."
"주식시장 호황을 타고 늘어난 빚투 자금도 부담 요인이다. 금융투자협회에 따르면 지난 26일 기준 신용거래융자 잔액은 36조2547억원으로 집계됐다. 지난 15일 36조5675억원으로 사상 최대치를 기록한 뒤에도 36조원대를 유지하고 있다. 예탁증권담보융자 잔액도 25조2816억원에 달했다. 신용거래융자와 예탁증권담보융자, 신용거래대주를 합친 증권사 신용공여 총액은 61조5797억원 규모다."
"시장에서는 향후 인상 폭과 속도에 따라 시장금리가 더 오를 수 있다는 전망도 나온다. 안예하 키움증권 애널리스트는 “반도체 중심의 수출 호조가 내수 개선으로 이어지고 물가 압력이 목표 수준을 웃도는 흐름이 지속된다면 내년 중 추가 인상을 통해 기준금리가 3.25% 이상으로 높아질 가능성도 열어둘 필요가 있다”며 “채권시장에서는 기준금리 인상 기대가 이미 상당 부분 반영됐음에도 시장금리의 하방보다 추가 상방 위험에 유의할 필요가 있다. 향후 인상 강도와 속도, 최종금리 수준에 대한 불확실성이 여전히 남아 있는 만큼 국고채 금리는 당분간 변동성이 높은 흐름을 이어갈 것”이라고 전망했다."
}

result = chain.invoke(input_text)
print("요약 결과: ", result['summary'])