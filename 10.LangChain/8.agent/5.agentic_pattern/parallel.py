from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
parser = StrOutputParser()

prompt_translate = ChatPromptTemplate.from_template(
"""
다음 영어 문장을 자연스러운 한국어로 번역하세요.

원문:
{original}

번역:
"""
)

llm1 = ChatOpenAI(model = "gpt-4o-mini", temperature=0.0)
llm2 = ChatOpenAI(model = "gpt-4o-mini", temperature=0.5)
llm3 = ChatOpenAI(model = "gpt-4o-mini", temperature=1.0)

translator1 = prompt_translate | llm1 | parser
translator2 = prompt_translate | llm2 | parser
translator3 = prompt_translate | llm3 | parser

translation_factory = RunnableParallel(
    candidate1=translator1,
    candidate2=translator2,
    candidate3=translator3
)

vote_prompt = ChatPromptTemplate.from_template(
"""
당신은 전문 번역 평가자입니다.

원문:
{original}

번역:
{translation}

다음 기준으로 평가하세요.

1. 의미 보존
- 원문의 의미와 의도를 얼마나 정확하게 전달하는가

2. 함축적 의미 전달
- 관용구, 비유, 문화적 표현의 의도를 제대로 살렸는가

3. 자연스러움
- 한국어 화자가 자연스럽게 읽을 수 있는가

4. 정보 누락/왜곡
- 중요한 의미가 빠지거나 잘못 전달되지 않았는가

평가 기준:
5 = 의미와 뉘앙스를 완벽히 전달
4 = 약간의 어색함은 있으나 의미 전달 우수
3 = 의미는 대체로 전달되나 뉘앙스 손실 존재
2 = 중요한 의미 손실 또는 오역 존재
1 = 의미 전달 실패

반드시 숫자 하나만 출력하세요.
"""
)
voter = vote_prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0.0) | parser

def pipeline_translate_and_vote(input_data: dict) -> str:
    original_text = input_data["original"]

    candidates = translation_factory.invoke({"original": original_text})
    
    best_candidate = None
    max_score = -1
    result_report = []
    
    for key, translation_text in candidates.items():
        score_str = voter.invoke({"original": original_text, "translation": translation_text})
        
        try:
            score = int(score_str.strip())
        except ValueError:
            score = 1
            
        result_report.append(f"[{key}] 번역: {translation_text.strip()} (평가점수: {score}점)")
        
        if score > max_score:
            max_score = score
            best_candidate = translation_text

    report_text = "\n".join(result_report)
    return f"\n[평가 리포트]\n{report_text}\n\n🏆 최종 선택된 번역: {best_candidate.strip()}"

translation_chain = RunnableLambda(pipeline_translate_and_vote)

test_sentence = {"original": "The squeaky wheel gets the grease."}
final_result = translation_chain.invoke(test_sentence)
print(final_result)