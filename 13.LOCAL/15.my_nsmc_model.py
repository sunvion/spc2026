# NSMC = Naver Sentiment Movie Corpus (네이버 영화 리뷰)

import numpy as np
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments
)
from datasets import load_dataset

MODEL = "beomi/KcBERT-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL)

# ds = load_dataset("nsmc", trust_remote_code=True)
ds = load_dataset("Blpeng/nsmc")

train_ds = ds["train"].filter(lambda x: bool(x["document"])).shuffle(seed=42).select(range(2000))
eval_ds = ds["test"].filter(lambda x: bool(x["document"])).shuffle(seed=42).select(range(500))

print(f"학습 데이터 수: {len(train_ds)}, 평가 데이터 수: {len(eval_ds)}")
print(f"예시: {train_ds[0]['document'][:30], {eval_ds[0]['document'][:30]}}")

# 🌟 [추가] 강사님 스타일의 토크나이징 함수 및 데이터셋 변환 🌟
# nsmc 데이터셋은 텍스트 컬럼 이름이 'document'이므로 x['document']로 맞춰줍니다.
def tokenize_function(x):
    return tokenizer(x['document'], padding="max_length", truncation=True)

# 텍스트 데이터를 모델이 이해할 수 있는 숫자 데이터셋으로 변환합니다.
train_tokenized = train_ds.map(tokenize_function, batched=True)
eval_tokenized = eval_ds.map(tokenize_function, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL, num_labels=2,
    id2label={0: "부정", 1: "긍정"},
    label2id={"부정": 0, "긍정": 1}
)

# 6. 평가지표 계산 함수 (오타 수정: matrics -> metrics)
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {"accuracy": float((preds == labels).mean())}

# 7. 학습 아규먼트 설정
args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    save_strategy="epoch",
    per_device_eval_batch_size=2,
    per_device_train_batch_size=2,
    num_train_epochs=5,
    logging_steps=1
)

# 8. 트레이너 정의 및 학습 시작
trainer = Trainer(
    model=model, 
    args=args,
    train_dataset=train_tokenized, 
    eval_dataset=eval_tokenized,
    compute_metrics=compute_metrics
)

trainer.train()

# 9. 평가 및 저장
print("\n[평가 결과]:", trainer.evaluate())