# pip install wcwidth

import json
import sys

# with open("history.json", "r", encoding="utf-8") as f;
#     messages = json.load(f)

# ROLE = {"humman": "사용자", "ai": "챗봇", "system": "시스템"}

# print(f"=== {len(messages)} 메시지 ===")
# for i, m in enumerate(messages, 1):
#     role = ROLE.get(m.get("type"), m.get("type"))
#     content = m.get("data").get("content")
#     print(f"{i:02d}. [{role:<4}] {content}")


with open("history.json", "r", encoding="utf-8") as f:
    messages = json.load(f)

ROLE = {
    "human": "사용자",
    "ai": "챗봇",
    "system": "시스템"
}

def pad_korean(text, width):
    """
    한글/영문 혼합 문자열을
    실제 출력 폭 기준으로 정렬
    """
    space = width - wcswidth(text)
    return text + (" " * max(space, 0))

print(f"=== {len(messages)} 메시지 ===")

for i, m in enumerate(messages, 1):
    role = ROLE.get(m.get("type"), m.get("type"))
    content = m.get("data", {}).get("content", "")

    role = pad_korean(role, 8)

    print(f"{i:02d}. [{role}] {content}")