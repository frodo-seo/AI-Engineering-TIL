"""with_tool_demo — 같은 질문에 tool 을 하나 붙이면 입력 토큰이 얼마나 늘어나나.

no_tool_demo.py 와 user 메시지는 동일. 차이는 payload 에 `tools` 가 붙는 것뿐.
tool 의 name / description / input_schema 가 전부 시스템 prefix 쪽에 직렬화되어
입력 토큰으로 환산된다 — 그래서 같은 user 메시지여도 input_tokens 가 커진다.
"""

import sys

from anthropic import Anthropic
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()
client = Anthropic()

MODEL = "claude-haiku-4-5-20251001"

tools = [
    {
        "name": "get_weather",
        "description": (
            "한국 도시의 현재 날씨를 조회한다. "
            "사용 시점: 사용자가 특정 도시 날씨를 물을 때."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "한국 도시명 (한글)",
                }
            },
            "required": ["city"],
        },
    }
]

payload = {
    "model": MODEL,
    "max_tokens": 256,
    "tools": tools,
    "messages": [
        {"role": "user", "content": "서울 날씨 알려줘"},
    ],
}

# ── 보내기 전: 모델이 받게 되는 입력 ────────────────────────────────
print(">>> tools (모델이 호출 가능하다고 알게 되는 함수 목록)")
for t in tools:
    print(f"  - {t['name']}: {t['description']}")

print("\n>>> messages content")
for m in payload["messages"]:
    print(m["content"])

# 같은 messages 로 tool 유/무 input_tokens 비교
n_no_tool = client.messages.count_tokens(
    model=MODEL,
    messages=payload["messages"],
).input_tokens

n_with_tool = client.messages.count_tokens(
    model=MODEL,
    tools=tools,
    messages=payload["messages"],
).input_tokens

print(f"\ninput_tokens (tool 없음) = {n_no_tool}")
print(f"input_tokens (tool 있음) = {n_with_tool}")
print(f"  → tool 정의로 늘어난 토큰 = {n_with_tool - n_no_tool}")

# ── 호출 ───────────────────────────────────────────────────────────
resp = client.messages.create(**payload)

print("\n<<< 모델 응답\n")
for block in resp.content:
    if block.type == "text":
        print(f"[text] {block.text}")
    elif block.type == "tool_use":
        print(f"[tool_use] {block.name}({block.input})")

print(f"\n[meta] stop_reason={resp.stop_reason}")
