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
다음 영어 문장을 자연스러운 한국어로 번역해줘.

[주의사항]
- 친절한 설명, 추가 해설, "~로 번역할 수 있습니다" 같은 군더더기 말은 절대로 하지 마세요.
- 오직 번역된 한국어 결과 문장 '딱 한 줄'만 출력하세요.

원문: {original}
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
당신은 번역 품질 평가자입니다. 다음 번역의 품질을 평가해주세요.

원문(영어): {original}
번역(한국어): {translation}

평가점수: 1~5점 (리커트 척도)
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