from transformers import pipeline

# Load the classification pipeline with the specified model
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

# Classify a new sentence
sentence = "I love this product! It's amazing and works perfectly."
result = pipe(sentence)

# Print the result
print(result)

reviews = [
    "배송도 빠르고 제품 품질도 기대 이상이라 정말 만족합니다.",
    "가격은 조금 비싸지만 성능이 좋아서 구매한 것을 후회하지 않습니다.",
    "사용 방법이 간단해서 누구나 쉽게 사용할 수 있을 것 같습니다.",
    "디자인은 예쁜데 생각보다 내구성이 약해서 아쉽습니다.",
    "배송이 너무 늦고 고객센터 연결도 어려워서 불편했습니다.",
    "제품이 설명과 달라서 실망했고 다시 구매할 생각은 없습니다.",
    "그냥 무난한 제품입니다. 특별히 좋지도 나쁘지도 않습니다.",
    "기능은 괜찮지만 가격을 생각하면 가성비가 좋은 편은 아닙니다.",
    "지금까지 사용해본 제품 중 가장 만족스럽습니다. 적극 추천합니다.",
    "처음에는 좋았는데 사용한 지 일주일 만에 고장이 나서 화가 납니다."
]

for review in reviews:
    result = pipe(review)
    print(f"리뷰: {review}")
    print(f"결과: {result}\n")