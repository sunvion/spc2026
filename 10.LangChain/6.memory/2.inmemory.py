from dotenv import load_dotenv

# 프롬프트
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# 모델
from langchain_openai import ChatOpenAI
# 파서
from langchain_core.output_parsers import StrOutputParser
# 기타
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

llm = ChatOpenAI(model = 'gpt-4o-mini')

prompt = ChatPromptTemplate.from_messages([
    ('system', "당신은 친절한 챗봇입니다."),
    MessagesPlaceholder('history'),
    ('user', "{input}")
])

chain = prompt | llm | StrOutputParser()

history = InMemoryChatMessageHistory()

def chat(message):
    print(f'질문: {message}')
    answer = chain.invoke({
        "input": message,
        # "history": history.messages, # 우리의 저장소에 있는 메시지 그대로 다
        "history": history.messages[-10:], # 최근 10개의 대화만 가져올 것
    })
    print(f'답변: {answer}')
    history.add_user_message(message)
    history.add_ai_message(answer)

chat("안녕하세요.")
chat("제 이름은 곽길동입니다.")
chat("저는 겨울에 바닷가에 가서 서핑하는 것을 좋아합니다.")
chat("제 이름과 취미가 뭐라고 했죠?")

questions = [
    """
    저는 어렸을 때부터 여행하는 것을 좋아했습니다. 특히 겨울 바다를 좋아해서 강릉, 속초, 부산, 제주도 같은 곳을 자주 다녔습니다.
    바닷가에서는 따뜻한 커피를 마시면서 파도 소리를 듣는 것을 좋아하고, 가끔은 새벽에 일어나 일출을 보기도 합니다.
    최근에는 서핑에도 관심이 생겨서 차가운 겨울 바다에서 서핑을 배우고 있습니다.
    """,

    """
    제가 최근에 읽은 책 중 가장 인상 깊었던 책은 인공지능과 인간의 미래에 대한 내용을 다룬 책이었습니다.
    그 책에서는 인간의 창의성과 AI의 계산 능력이 어떻게 협력할 수 있는지 설명하고 있었고,
    특히 교육 분야에서 AI 튜터가 학생 개개인의 학습 속도에 맞춰 도움을 줄 수 있다는 점이 흥미로웠습니다.
    또한 미래에는 대부분의 반복 업무가 자동화될 가능성이 높다고 이야기했습니다.
    """,

    """
    제가 좋아하는 음식은 정말 다양합니다. 한식 중에서는 김치찌개, 된장찌개, 불고기, 비빔밥을 좋아하고,
    양식 중에서는 파스타와 피자를 자주 먹습니다. 특히 크림 파스타보다는 오일 파스타를 더 선호합니다.
    디저트로는 티라미수와 치즈케이크를 좋아하고, 음료는 아이스 아메리카노를 거의 매일 마십니다.
    """,

    """
    운동도 여러 가지를 해봤는데, 헬스장에서는 주로 러닝머신과 스쿼트를 하고,
    주말에는 한강에서 자전거를 타거나 친구들과 배드민턴을 치곤 합니다.
    최근에는 수영도 배우기 시작했는데 자유형 호흡이 아직 익숙하지 않아서 연습 중입니다.
    운동을 하고 나면 몸은 힘들지만 정신적으로 훨씬 개운해지는 느낌이 들어서 꾸준히 하려고 노력하고 있습니다.
    """,

    """
    프로그래밍 공부도 꾸준히 하고 있습니다. Python, JavaScript, SQL을 공부했고,
    최근에는 LangChain과 RAG 시스템 구축에 관심이 많습니다.
    OpenAI API를 사용해서 챗봇을 만들거나 PDF 기반 질의응답 시스템을 만드는 실습을 자주 하고 있습니다.
    벡터 데이터베이스와 임베딩 모델의 차이점도 공부하고 있고, 프롬프트 엔지니어링에도 흥미를 느끼고 있습니다.
    """,

    """
    제가 가장 기억에 남는 여행은 제주도 여행이었습니다.
    첫날에는 협재 해수욕장에서 노을을 봤고, 둘째 날에는 성산일출봉에 새벽에 올라가서 일출을 감상했습니다.
    셋째 날에는 우도에 들어가서 전기 자전거를 타고 섬을 한 바퀴 돌았습니다.
    특히 겨울 제주 바다는 차갑지만 사람이 많지 않아서 조용하고 평화로운 분위기가 정말 좋았습니다.
    """
]

for q in questions :
    chat(q)

chat("제 이름과 취미가 뭐라고 했죠?")