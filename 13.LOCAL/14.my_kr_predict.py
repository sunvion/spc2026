import os
from transformers import pipeline

# 본인이 저장한 한국어 모델 폴더명으로 매칭해 주세요 (예: ./my_local_kr_model)
MODEL_DIR = "./my_local_kr_model" 

# 감성 분석(sentiment-analysis) 파이프라인 생성
classifier = pipeline("sentiment-analysis", model=MODEL_DIR, tokenizer=MODEL_DIR)

# 테스트할 한국어 문장들
test_sentences = [
    "내가 직접 만든 AI 모델을 쓰니까 정말 뿌듯하다!",
    "진짜 살면서 겪은 일 중 최악의 경험이었어.",
    "와, 기대 안 했는데 생각보다 너무 최고인 듯?",
    "기분이 너무 안 좋고 속상해..."
]

print("=== 한국어 모델 추론 결과 ===")
for text in test_sentences:
    r = classifier(text)[0]
    # 소수점 4자리까지 확률(score)도 함께 출력되도록 구성했습니다.
    print(f"문장: {text}")
    print(f"결과: {r['label']} (신뢰도: {r['score']:.4f})\n")