"""Phase 2 블록 A — Tool use 기본 흐름 (입출력 가시화 버전).

매 API 호출마다:
  - INPUT  : messages 배열을 그대로 덤프 (어떤 role / 어떤 블록 type 이 쌓였는지)
  - OUTPUT : stop_reason, usage, 모든 content 블록을 type 별로 덤프

이걸로 보고 싶은 것:
  1. 1차 호출의 input(=user 메시지 1개)에서 모델이 tool_use 블록을 어떻게 내는가
  2. 그 tool_use 블록을 messages 에 그대로 다시 넣고, tool_result 까지 붙인
     2차 호출의 input 이 어떻게 생겼는가
  3. 그 input 을 받은 모델이 최종 text 답변을 어떻게 생성하는가
  4. description 의 "사용 안 함" 이 실제로 1차에서 도구 호출을 막는가
"""

import json
import sys

from anthropic import Anthropic
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
client = Anthropic()


# ── mock 도구 ───────────────────────────────────────────────────
WEATHER_DB = {
    "서울": "맑음, 22°C, 풍속 약함",
    "부산": "흐림, 25°C, 약간의 비",
    "제주": "비, 19°C, 강풍",
}


def get_weather(city: str) -> str:
    if city in WEATHER_DB:
        return WEATHER_DB[city]
    return (
        f"'{city}' 의 날씨 데이터가 없습니다. "
        f"이 도구는 다음 도시만 지원합니다: {', '.join(WEATHER_DB)}. "
        f"사용자에게 지원 도시를 안내하거나 다른 도시를 요청하세요."
    )


tools = [
    {
        "name": "get_weather",
        "description": (
            "한국 주요 도시의 현재 날씨를 조회한다. "
            "사용 시점: 사용자가 특정 도시의 날씨·기온·강수를 물을 때. "
            "사용 안 함: 미래 예보, 해외 도시. 그 경우 도구를 부르지 말고 "
            "답할 수 없음을 사용자에게 알려라. "
            "결과: '날씨, 기온, 풍속/강수' 형태의 한 줄 텍스트, "
            "또는 데이터 없음 안내."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "한국 도시명 (한글). 예: '서울', '부산', '제주'.",
                }
            },
            "required": ["city"],
        },
    }
]


# ── 가시화 헬퍼 ─────────────────────────────────────────────────
def _short(s: str, n: int = 200) -> str:
    s = str(s)
    return s if len(s) <= n else s[:n] + f"... <+{len(s)-n} chars>"


def _block_to_str(block) -> str:
    """dict(우리가 만든 메시지) 와 SDK 객체(모델 응답) 둘 다 처리."""
    if isinstance(block, dict):
        btype = block.get("type", "?")
        if btype == "text":
            return f"text: {_short(block.get('text', ''))!r}"
        if btype == "tool_use":
            return (
                f"tool_use: name={block.get('name')} "
                f"input={json.dumps(block.get('input'), ensure_ascii=False)} "
                f"id={block.get('id')}"
            )
        if btype == "tool_result":
            return (
                f"tool_result: tool_use_id={block.get('tool_use_id')} "
                f"content={_short(block.get('content', ''))!r}"
            )
        return f"{btype}: {block}"
    btype = getattr(block, "type", "?")
    if btype == "text":
        return f"text: {_short(block.text)!r}"
    if btype == "tool_use":
        return (
            f"tool_use: name={block.name} "
            f"input={json.dumps(block.input, ensure_ascii=False)} "
            f"id={block.id}"
        )
    return f"{btype}: {block}"


def dump_messages_input(messages, label: str) -> None:
    print(f"\n┌── INPUT: {label}  (messages = {len(messages)} item)")
    for i, m in enumerate(messages):
        role = m["role"]
        content = m["content"]
        if isinstance(content, str):
            print(f"│  [{i}] role={role}  → string: {_short(content)!r}")
            continue
        print(f"│  [{i}] role={role}  → blocks ({len(content)}):")
        for j, block in enumerate(content):
            print(f"│       ({j}) {_block_to_str(block)}")
    print("└" + "─" * 70)


def dump_response_output(resp, label: str) -> None:
    print(f"\n┌── OUTPUT: {label}")
    print(f"│  stop_reason = {resp.stop_reason}")
    print(
        f"│  usage = input:{resp.usage.input_tokens} "
        f"output:{resp.usage.output_tokens} "
        f"(cache_read:{getattr(resp.usage, 'cache_read_input_tokens', 0)} "
        f"cache_create:{getattr(resp.usage, 'cache_creation_input_tokens', 0)})"
    )
    print(f"│  content blocks ({len(resp.content)}):")
    for i, block in enumerate(resp.content):
        print(f"│    [{i}] {_block_to_str(block)}")
    print("└" + "─" * 70)


# ── 한 턴 핑퐁 실행기 ───────────────────────────────────────────
def run(user_message: str) -> None:
    print("\n" + "=" * 72)
    print(f" USER QUERY: {user_message!r}")
    print("=" * 72)

    messages = [{"role": "user", "content": user_message}]

    # ── 1차 호출 ────────────────────────────────────────────────
    dump_messages_input(messages, "1차 호출")
    resp = client.messages.create(
        model=MODEL, max_tokens=512, tools=tools, messages=messages
    )
    dump_response_output(resp, "1차 호출")

    # 도구 안 쓰고 바로 답한 경우 → 종료
    if resp.stop_reason != "tool_use":
        print("\n  ▶ 도구 미사용. 1차에서 종료.")
        return

    # assistant 응답을 messages 에 그대로 누적 (tool_use 블록 포함)
    messages.append({"role": "assistant", "content": resp.content})

    # tool_use 블록 → 실제 함수 실행 → tool_result 모음
    print("\n  ▶ LOCAL EXECUTION (모델이 부른 도구를 우리가 실제 실행):")
    tool_results = []
    for block in resp.content:
        if block.type == "tool_use":
            if block.name == "get_weather":
                output = get_weather(**block.input)
            else:
                output = f"Unknown tool: {block.name}"
            print(f"      {block.name}({json.dumps(block.input, ensure_ascii=False)})  →  {output!r}")
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                }
            )

    # tool_result 를 user 역할로 회신
    messages.append({"role": "user", "content": tool_results})

    # ── 2차 호출 ────────────────────────────────────────────────
    dump_messages_input(messages, "2차 호출 (assistant tool_use + user tool_result 추가됨)")
    final = client.messages.create(
        model=MODEL, max_tokens=512, tools=tools, messages=messages
    )
    dump_response_output(final, "2차 호출 (최종)")


if __name__ == "__main__":
    # 1) 정상 케이스
    run("서울 날씨 어때?")
    # 2) 도구가 에러 메시지를 반환하는 케이스 (한국 도시지만 DB 에 없음)
    run("평창 날씨 알려줘")
    # 3) description 의 "사용 안 함: 해외 도시" 가 도구 호출을 막는지 확인
    run("도쿄 날씨 어때?")
