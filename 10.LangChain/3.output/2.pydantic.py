from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field

load_dotenv()

class MovieReview(BaseModel):
    """ 영화 리뷰 분석 결과 """
    title: str = Field(description = "영화 제목")
    sentiment: str = Field(description = "감성 분류: 긍정, 부정, 중립")
    score: int = Field(description = "1~10 점수")
    summary: str = Field(description = "리뷰 요약 (1~2문장)")
    keywords: list[str] = Field(description = "핵심 키워드 3개")

llm = ChatOpenAI(model="gpt-4o-mini")

parser = PydanticOutputParser(pydantic_object=MovieReview)
# print('포멧 명령문:')
# print(parser.get_format_instructions())

prompt = ChatPromptTemplate.from_template(
    """ 다음 영화 리뷰를 분석해주세요.
리뷰:{review}

{format_instructions}
"""
)

chain = prompt | llm | parser

reviews = [
    "《아바타: 불과 재》: 제임스 카메론 감독의 삼편작으로, 이번에는 파괴적인 '재의 부족'을 통해 나비족의 어두운 이면을 비추며 판도라의 세계관을 한 단계 더 확장합니다. 한층 더 진화한 시각 효과는 눈을 즐겁게 하고, 환경과 평화에 대한 묵직한 메시지는 깊은 여운을 남깁니다. 시각적 전율과 감정적 몰입을 동시에 선사하는 명작입니다.",
    "《미키 17》: 봉준호 감독과 로버트 패틴슨이 호흡을 맞춘 SF 블랙 코미디로, 얼음 행성을 개척하는 복제인간의 삶과 죽음을 다룹니다. 인간의 존엄성과 자본주의의 모순을 봉 감독 특유의 디스토피아적 유머와 날카로운 시선으로 풍자해 냈습니다. 예측 불가능한 전개와 독창적인 연출이 돋보이는 강렬한 작품입니다.",
    "《주토피아 2》: 디즈니의 인기 콤비 주디와 닉이 도시를 뒤흔드는 미스터리한 사건을 해결하기 위해 새로운 파트너십을 발휘하며 돌아왔습니다. 전편의 매력을 고스란히 이어받아 현대 사회의 편견과 공존이라는 주제를 영리하고 따뜻하게 풀어냈습니다. 더 다양해진 동물 캐릭터들과 화려해진 볼거리로 전 세대 관객을 사로잡았습니다."
]

for review in reviews:
    result = chain.invoke({
        "review": review,
        "format_instructions": parser.get_format_instructions()
    })

    print(f"제목: {result.title}")
    print(f"감성: {result.sentiment} (점수: {result.score}/10)")
    print(f"요약: {result.summary}")
    print(f"키워드: {result.keywords}")
    print("-"*30)