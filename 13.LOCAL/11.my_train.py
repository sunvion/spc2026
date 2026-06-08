# 나만의 데이터로 모델 추가 학습하기 (fine-tuning)
# pip install transformers torch datasets
# pip install -U accelerate transformers

import numpy as np
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments
)
from datasets import Dataset

# 1. 데이터셋 준비 (오타 수정: Morst -> Worst)
train_data = {
    "text": ["I love this!", "This is terrible!", "I am happy", "I am sad", "This product is amazing", "Worst experience ever", "Absolutely fantastic", "I hate it."],
    "label": [1, 0, 1, 0, 1, 0, 1, 0]
}

eval_data = {
    "text": ["I feel greater today!", "The service was awful", "I'm super excited about this!", "Not what I expected"],
    "label": [1, 0, 1, 0]
}

# 2. 토크나이저 및 모델 로드
model_name = "distilbert-base-uncased"
model_tokenizer = AutoTokenizer.from_pretrained(model_name)

# 3. 토크나이징 함수 정의 (함수 이름 중복 방지를 위해 토크나이저 객체명과 분리)
def tokenize_function(batch):
    return model_tokenizer(batch['text'], padding="max_length", truncation=True)

# 4. Dataset 변환 및 매핑
train_ds = Dataset.from_dict(train_data).map(tokenize_function, batched=True)
eval_ds = Dataset.from_dict(eval_data).map(tokenize_function, batched=True)

# 5. 분류 모델 생성
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=2,
    id2label={0: "NEGATIVE", 1: "POSITIVE"},
    label2id={"NEGATIVE": 0, "POSITIVE": 1}
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
    train_dataset=train_ds, 
    eval_dataset=eval_ds,
    compute_metrics=compute_metrics
)

trainer.train()

# 9. 평가 및 저장
print("\n[평가 결과]:", trainer.evaluate())

save_path = "./my_local_model"
model.save_pretrained(save_path)
model_tokenizer.save_pretrained(save_path)

print(f"\n모델 및 토크나이저 저장 완료: {save_path}")