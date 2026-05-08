"""no_tool_demo — tool 없이 그냥 물어보면 어떻게 되나.

여기서 보고 싶은 것:
  1. 모델이 실시간 날씨 같은 외부 정보를 모른다는 사실을 어떻게 표현하는지.
  2. tool 없이 보내는 가장 단순한 payload 가 어떻게 생겼는지.
  3. 그 payload 가 입력 토큰 몇 개로 환산되는지.

이 단계에서 "왜 tool 이 필요한가" 가 자연스럽게 나온다.
"""

import sys

from anthropic import Anthropic
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()
client = Anthropic()

MODEL = "claude-haiku-4-5-20251001"

payload = {
    "model": MODEL,
    "max_tokens": 256,
    "messages": [
        {"role": "user", "content": "서울 날씨 알려줘"},
    ],
}

# ── 보내기 전: 모델이 받게 되는 입력 ────────────────────────────────
print(">>> messages content")
for m in payload["messages"]:
    print(m["content"])

n_in = client.messages.count_tokens(
    model=MODEL,
    messages=payload["messages"],
).input_tokens
print(f"\ninput_tokens = {n_in}")

# ── 호출 ───────────────────────────────────────────────────────────
resp = client.messages.create(**payload)

print("\n<<< 모델 응답\n")
for block in resp.content:
    if block.type == "text":
        print(block.text)

print(f"\n[meta] stop_reason={resp.stop_reason}")
