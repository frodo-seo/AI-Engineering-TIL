"""Phase 2 블록 A — Tool chain (도구 결과가 다음 도구 인자로).

흐름 예상:
  user: "단풍 구경하기 좋은 도시 하나 추천해주고, 그 도시 지금 날씨도 알려줘"
    │
    ├─ 호출 #1 → tool_use: recommend_city(theme="단풍")          ← 모델 결정
    │           우리: recommend_city("단풍") → "속초"
    │
    ├─ 호출 #2 → tool_use: get_weather(city="속초")              ← 1차 결과를 인자로
    │           우리: get_weather("속초") → "맑음, 18°C..."
    │
    └─ 호출 #3 → end_turn (자연어 최종 답변)

학습 포인트:
  1. 모델이 turn 마다 tool_use / end_turn 을 자율적으로 결정 — 우리는 loop 만 돌림
  2. 매 호출마다 messages 누적 + tools 정의 매번 재전송
     → input_tokens 가 계속 증가하는 걸 끝의 TOKEN SUMMARY 표로 정량 관찰
  3. MAX_ITER 안전장치 — 모델이 무한 루프 도는 걸 막는 실전 패턴
"""

import json
import sys

from anthropic import Anthropic
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
MAX_ITER = 10
client = Anthropic()


# ── mock 도구 데이터 ───────────────────────────────────────────
DESTINATIONS = {
    "단풍": "속초",
    "벚꽃": "진해",
    "야경": "부산",
    "온천": "충주",
}

WEATHER_DB = {
    "속초": "맑음, 18°C, 풍속 약함",
    "진해": "흐림, 21°C, 약간의 비",
    "부산": "맑음, 24°C, 풍속 약함",
    "충주": "구름, 16°C, 풍속 약함",
}


def recommend_city(theme: str) -> str:
    if theme in DESTINATIONS:
        return f"'{theme}' 테마 추천 도시: {DESTINATIONS[theme]}"
    return (
        f"'{theme}' 테마 매칭 도시 없음. "
        f"지원 테마: {', '.join(DESTINATIONS)}. 사용자에게 다른 테마를 요청하세요."
    )


def get_weather(city: str) -> str:
    if city in WEATHER_DB:
        return WEATHER_DB[city]
    return (
        f"'{city}' 의 날씨 데이터 없음. "
        f"지원 도시: {', '.join(WEATHER_DB)}. 사용자에게 안내하세요."
    )


TOOLS_IMPL = {
    "recommend_city": recommend_city,
    "get_weather": get_weather,
}

tools = [
    {
        "name": "recommend_city",
        "description": (
            "특정 테마(예: 단풍, 벚꽃, 야경, 온천)에 어울리는 한국 도시 한 곳을 추천한다. "
            "사용 시점: 사용자가 도시를 정하지 않은 채 '~하기 좋은 곳' 을 물을 때. "
            "사용 안 함: 사용자가 이미 도시를 명시한 경우. "
            "결과: 추천 도시명을 포함한 한 줄 텍스트."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "theme": {
                    "type": "string",
                    "description": "추천 테마 (한글). 예: '단풍', '벚꽃', '야경', '온천'.",
                }
            },
            "required": ["theme"],
        },
    },
    {
        "name": "get_weather",
        "description": (
            "한국 도시의 현재 날씨를 조회한다. "
            "사용 시점: 사용자가 특정 도시의 날씨·기온·강수를 물을 때, "
            "또는 다른 도구의 결과로 도시명이 정해졌고 그 도시의 날씨가 필요할 때. "
            "사용 안 함: 미래 예보, 해외 도시. "
            "결과: '날씨, 기온, 풍속/강수' 한 줄 텍스트."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "한국 도시명 (한글). 예: '속초', '부산'.",
                }
            },
            "required": ["city"],
        },
    },
]


# ── 가시화 헬퍼 ────────────────────────────────────────────────
def _short(s, n=200):
    s = str(s)
    return s if len(s) <= n else s[:n] + f"... <+{len(s)-n} chars>"


def _block_to_str(block) -> str:
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


def dump_input(messages, label):
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


def dump_output(resp, label):
    print(f"\n┌── OUTPUT: {label}")
    print(f"│  stop_reason = {resp.stop_reason}")
    print(
        f"│  usage = input:{resp.usage.input_tokens} "
        f"output:{resp.usage.output_tokens}"
    )
    print(f"│  content blocks ({len(resp.content)}):")
    for i, block in enumerate(resp.content):
        print(f"│    [{i}] {_block_to_str(block)}")
    print("└" + "─" * 70)


# ── 실행 루프 (chain 의 핵심) ──────────────────────────────────
def run(user_message: str) -> None:
    print("\n" + "=" * 72)
    print(f" USER QUERY: {user_message!r}")
    print("=" * 72)

    messages = [{"role": "user", "content": user_message}]
    usages = []

    for iteration in range(1, MAX_ITER + 1):
        dump_input(messages, f"호출 #{iteration}")
        resp = client.messages.create(
            model=MODEL, max_tokens=512, tools=tools, messages=messages
        )
        dump_output(resp, f"호출 #{iteration}")
        usages.append((resp.usage.input_tokens, resp.usage.output_tokens))

        if resp.stop_reason == "end_turn":
            print(f"\n  ▶ end_turn 도달. 총 {iteration} 회 호출.")
            break

        if resp.stop_reason != "tool_use":
            print(f"\n  ▶ 예상 못 한 stop_reason: {resp.stop_reason}. 종료.")
            break

        # 모델 응답을 messages 에 누적
        messages.append({"role": "assistant", "content": resp.content})

        # 모델이 부른 tool_use 들을 우리가 실제로 실행
        print("\n  ▶ LOCAL EXECUTION:")
        tool_results = []
        for block in resp.content:
            if block.type == "tool_use":
                impl = TOOLS_IMPL.get(block.name)
                output = impl(**block.input) if impl else f"Unknown tool: {block.name}"
                print(
                    f"      {block.name}({json.dumps(block.input, ensure_ascii=False)})"
                    f"  →  {output!r}"
                )
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": output,
                    }
                )
        messages.append({"role": "user", "content": tool_results})
    else:
        print(f"\n  ▶ MAX_ITER ({MAX_ITER}) 도달. 강제 종료.")

    # 호출별 토큰 비교 — chain 이 길어질수록 input 이 어떻게 늘어나는지 정량 확인
    print("\n  ▶ TOKEN SUMMARY (호출별):")
    print(f"      {'#':<5}{'input':>10}{'output':>10}")
    for i, (ti, to) in enumerate(usages, 1):
        print(f"      {i:<5}{ti:>10}{to:>10}")
    total_in = sum(t[0] for t in usages)
    total_out = sum(t[1] for t in usages)
    print(f"      {'합계':<5}{total_in:>10}{total_out:>10}")


if __name__ == "__main__":
    run("단풍 구경하기 좋은 도시 하나 추천해주고, 그 도시 지금 날씨도 알려줘")
