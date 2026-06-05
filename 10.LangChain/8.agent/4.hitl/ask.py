from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage

load_dotenv()

# =========================
# 데이터
# =========================

accounts = {
    "alice": 1_000_000,
    "bob": 500_000,
}

transactions = []

# =========================
# 메모리
# =========================

checkpoint = MemorySaver()

# =========================
# Tools
# =========================

@tool
def send_payment(recipient: str, amount: int) -> str:
    """수신자에게 지정 금액을 송금한다."""

    sender = "alice"

    if recipient not in accounts:
        return f"{recipient} 계좌가 존재하지 않습니다."

    if accounts[sender] < amount:
        return "잔액이 부족합니다."

    accounts[sender] -= amount
    accounts[recipient] += amount

    transactions.append(
        {
            "type": "송금",
            "from": sender,
            "to": recipient,
            "amount": amount,
        }
    )

    return f"{recipient}에게 {amount:,}원 송금 완료"


@tool
def get_balance(account: str) -> str:
    """계좌 잔액 조회"""

    balance = accounts.get(account)

    if balance is None:
        return "계좌가 존재하지 않습니다."

    return f"{account} 계좌 잔액은 {balance:,}원입니다."


@tool
def deposit(account: str, amount: int) -> str:
    """계좌에 입금한다."""

    if account not in accounts:
        return "계좌가 존재하지 않습니다."

    accounts[account] += amount

    transactions.append(
        {
            "type": "입금",
            "account": account,
            "amount": amount,
        }
    )

    return f"{account} 계좌에 {amount:,}원 입금 완료"


@tool
def withdraw(account: str, amount: int) -> str:
    """계좌에서 출금한다."""

    if account not in accounts:
        return "계좌가 존재하지 않습니다."

    if accounts[account] < amount:
        return "잔액이 부족합니다."

    accounts[account] -= amount

    transactions.append(
        {
            "type": "출금",
            "account": account,
            "amount": amount,
        }
    )

    return f"{account} 계좌에서 {amount:,}원 출금 완료"


@tool
def get_transactions() -> str:
    """최근 거래 내역 조회"""

    if not transactions:
        return "거래 내역이 없습니다."

    result = []

    for idx, tx in enumerate(transactions, start=1):
        result.append(f"{idx}. {tx}")

    return "\n".join(result)


# =========================
# LLM
# =========================

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_agent(
    llm,
    [
        send_payment,
        get_balance,
        deposit,
        withdraw,
        get_transactions,
    ],
    checkpointer=checkpoint,
    interrupt_before=["tools"],
)

config = {
    "configurable": {
        "thread_id": "t001"
    }
}

print("=" * 50)
print("금융 챗봇 시작")
print("종료 입력 시 종료")
print("=" * 50)

while True:

    question = input("\n[유저] ").strip()

    if question.lower() in ["종료", "exit", "quit"]:
        print("프로그램 종료")
        break

    result = agent.invoke(
        {"messages": [("user", question)]},
        config=config,
    )

    state = agent.get_state(config)

    messages = state.values["messages"]

    ai_msg = messages[-1]

    # Tool 호출이 없는 경우
    if not getattr(ai_msg, "tool_calls", None):
        final = ai_msg.content
        print(f"[챗봇] {final}")
        continue

    # Tool 호출이 있는 경우
    call = ai_msg.tool_calls[0]

    print("\n" + "=" * 30)
    print(f"[에이전트 제안]")
    print(f"Tool : {call['name']}")
    print(f"Args : {call['args']}")
    print("=" * 30)

    # 송금일 때만 승인 절차
    if call["name"] == "send_payment":

        args = call["args"]

        print(
            f"\n{args['recipient']}에게 "
            f"{args['amount']:,}원을 송금하시겠습니까?"
        )

        print("1. 예")
        print("2. 아니오")
        print("3. 금액 수정")

        choice = input("선택 (1/2/3): ").strip()

        if choice == "2":
            print("\n[취소] 사용자 요청에 의해 취소되었습니다.")
            continue

        if choice == "3":

            new_amount = int(
                input("새 송금 금액(원)을 입력하세요: ").strip()
            )

            edited = {
                **call,
                "args": {
                    **call["args"],
                    "amount": new_amount,
                },
            }

            fixed = AIMessage(
                content=ai_msg.content,
                tool_calls=[edited],
                id=ai_msg.id,
            )

            agent.update_state(
                config,
                {"messages": [fixed]},
            )

            print(
                f"사람이 수정함: "
                f"{args['amount']} -> {new_amount}"
            )

    # 이어서 실행
    result = agent.invoke(None, config=config)

    final = result["messages"][-1].content

    if not final:
        final = result["messages"][-2].content

    print(f"\n[최종] {final}")