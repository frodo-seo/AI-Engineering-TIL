"""Phase 2 블록 B — Structured Output (Pydantic).

핵심 학습:
  같은 tool calling 인프라를 "출력 형식 강제 contract" 로 재사용한다.
  도구를 정의하지만 *실행하지 않음* — tool_use.input 자체가 우리가 원하는 결과.

비교:
  Part A — 자연어 응답 (강제 없음)   : prompt 로 "JSON 으로 줘" 부탁만 함
  Part B — schema 강제 (tool calling): Pydantic schema 를 input_schema 로 등록
                                        + tool_choice 로 그 도구 무조건 호출
"""

import json
import sys
from datetime import date

from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()
MODEL = "claude-haiku-4-5-20251001"
client = Anthropic()


# ── 우리가 원하는 결과 schema (Pydantic 모델) ──────────────────
class Event(BaseModel):
    title: str
    event_date: date          # ← date 객체로 자동 파싱되는지 확인 포인트
    location: str
    speakers: list[str]
    tags: list[str]


# ── 입력 텍스트 (자유 형식 자연어) ──────────────────────────────
EVENT_TEXT = """
🎉 AI Engineer Summit 2026

2026년 5월 12일 (화), 서울 코엑스 A홀에서 개최합니다.

키노트 발표자:
  • Andrej Karpathy
  • Lilian Weng
  • Harrison Chase

세션 주제: LLM, agents, evals, RAG
"""


# ── Part A — 자연어 응답 (강제 없음) ───────────────────────────
def part_a_natural_language() -> None:
    print("\n" + "=" * 72)
    print(" PART A — 자연어 응답 (schema 강제 없음, prompt 로 부탁만)")
    print("=" * 72)

    schema_str = json.dumps(Event.model_json_schema(), ensure_ascii=False, indent=2)
    user_msg = (
        f"아래 텍스트에서 이벤트 정보를 추출해 JSON 으로만 응답해. "
        f"코드펜스나 부가 설명 없이 JSON 본문만.\n\n"
        f"<text>\n{EVENT_TEXT}\n</text>\n\n"
        f"JSON schema:\n{schema_str}"
    )

    resp = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": user_msg}],
    )

    raw = "".join(b.text for b in resp.content if b.type == "text")
    print(
        f"\n[OUTPUT] stop_reason={resp.stop_reason}  "
        f"in={resp.usage.input_tokens} out={resp.usage.output_tokens}"
    )
    print(f"[RAW TEXT]\n{raw}")

    print("\n[PARSE 시도]")
    try:
        data = json.loads(raw)
        print(f"  json.loads OK")
    except json.JSONDecodeError as e:
        print(f"  json.loads FAIL: {e}")
        print("  ▶ 자연어 응답은 보장이 없음. 코드펜스, 부가 설명, 따옴표 변형 등으로 깨질 수 있음.")
        return

    try:
        event = Event.model_validate(data)
        print(f"  Pydantic OK → {event!r}")
        print(f"  event.event_date type = {type(event.event_date).__name__}")
    except ValidationError as e:
        print(f"  Pydantic ValidationError:\n{e}")


# ── Part B — schema 강제 (tool calling 트릭) ──────────────────
def part_b_structured_output() -> None:
    print("\n" + "=" * 72)
    print(" PART B — schema 강제 (tool calling 트릭)")
    print("=" * 72)

    # 핵심 트릭 (1): Pydantic 이 만든 JSON schema 를 그대로 input_schema 로
    tools = [
        {
            "name": "submit_event",
            "description": (
                "추출된 이벤트 정보를 제출한다. "
                "텍스트에 명시된 정보만 사용하고 추측 금지."
            ),
            "input_schema": Event.model_json_schema(),
        }
    ]

    user_msg = (
        f"아래 텍스트에서 이벤트 정보를 추출해 submit_event 를 호출해라.\n\n"
        f"<text>\n{EVENT_TEXT}\n</text>"
    )

    # 핵심 트릭 (2): tool_choice 로 무조건 그 도구 호출 강제
    resp = client.messages.create(
        model=MODEL,
        max_tokens=512,
        tools=tools,
        tool_choice={"type": "tool", "name": "submit_event"},
        messages=[{"role": "user", "content": user_msg}],
    )

    print(
        f"\n[OUTPUT] stop_reason={resp.stop_reason}  "
        f"in={resp.usage.input_tokens} out={resp.usage.output_tokens}"
    )
    print(f"[CONTENT BLOCKS] {len(resp.content)} 개")
    for i, block in enumerate(resp.content):
        if block.type == "tool_use":
            print(f"  [{i}] tool_use: name={block.name}  id={block.id}")
            print(f"        input (= 우리가 원하는 결과 dict):")
            print(json.dumps(block.input, ensure_ascii=False, indent=8))
        elif block.type == "text":
            print(f"  [{i}] text: {block.text!r}")

    # tool_use.input 을 Pydantic 으로 검증 + 변환
    tool_use_block = next(b for b in resp.content if b.type == "tool_use")
    print("\n[Pydantic 변환]")
    try:
        event = Event.model_validate(tool_use_block.input)
        print("  ✓ Event 객체 생성 성공")
        print(f"     title       = {event.title!r}")
        print(
            f"     event_date  = {event.event_date!r}  "
            f"(type={type(event.event_date).__name__})"
        )
        print(f"     location    = {event.location!r}")
        print(f"     speakers    = {event.speakers!r}")
        print(f"     tags        = {event.tags!r}")
    except ValidationError as e:
        print(f"  ✗ ValidationError:\n{e}")

    print("\n  ▶ 주목: submit_event 함수를 우리가 만든 적도, 부른 적도 없다.")
    print("    tool 정의는 schema contract 역할만. tool_use.input 자체가 결과.")


if __name__ == "__main__":
    part_a_natural_language()
    part_b_structured_output()
