# 나만의 한국어 데이터로 모델 추가 학습하기 (fine-tuning)
# pip install transformers torch datasets accelerate

import numpy as np
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments
)
from datasets import Dataset

# 1. 한국어 데이터셋 준비 (0: 부정, 1: 긍정)
train_data = {
    "text": [
        "이 제품 진짜 마음에 들어요!", 
        "돈 버렸네요. 절대 사지 마세요.", 
        "오늘 기분이 너무 좋아요.", 
        " 너무 슬프고 우울한 하루입니다.", 
        "배송도 빠르고 상품 상태도 최고입니다.", 
        "최악의 경험이었어요. 서비스 엉망임.", 
        "정말 대만족입니다. 강력 추천해요!", 
        "진짜 짜증나고 실망스럽네요."
    ],
    "label": [1, 0, 1, 0, 1, 0, 1, 0]
}

eval_data = {
    "text": [
        "오늘 생각보다 날씨도 좋고 행복하네요!", 
        "고객센터 불친절해서 기분 잡쳤어요.", 
        "기대 이상으로 정말 멋진 상품입니다.", 
        "생각했던 것보다 별로예요."
    ],
    "label": [1, 0, 1, 0]
}

# 2. 한국어 지원 모델 및 토크나이저 로드
# 여기서는 가장 대중적인 다국어 BERT 모델을 사용합니다. (또는 'klue/bert-base' 추천)
model_name = "beomi/kcbert-base"
model_tokenizer = AutoTokenizer.from_pretrained(model_name)

# 3. 토크나이징 함수 정의
def tokenize_function(batch):
    return model_tokenizer(batch['text'], padding="max_length", truncation=True)

# 4. Dataset 변환 및 매핑
train_ds = Dataset.from_dict(train_data).map(tokenize_function, batched=True)
eval_ds = Dataset.from_dict(eval_data).map(tokenize_function, batched=True)

# 5. 분류 모델 생성 (한국어 라벨 매핑)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=2,
    id2label={0: "부정", 1: "긍정"},
    label2id={"부정": 0, "긍정": 1}
)

# 6. 평가지표 계산 함수
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {"accuracy": float((preds == labels).mean())}

# 7. 학습 아규먼트 설정
args = TrainingArguments(
    output_dir="./results_kr",
    eval_strategy="epoch",
    save_strategy="epoch",
    per_device_eval_batch_size=2,
    per_device_train_batch_size=2,
    num_train_epochs=20,
    logging_steps=1
)

# 8. 트레이너 정의 및 학습 시작
trainer = Trainer(
    model=model, 
    args=args,
    train_dataset=train_ds, 
    eval_dataset=eval_ds,
    compute_metrics=compute_metrics
)

trainer.train()

# 9. 평가 및 저장
print("\n[평가 결과]:", trainer.evaluate())

save_path = "./my_local_ko_model"
model.save_pretrained(save_path)
model_tokenizer.save_pretrained(save_path)

print(f"\n한국어 모델 및 토크나이저 저장 완료: {save_path}")