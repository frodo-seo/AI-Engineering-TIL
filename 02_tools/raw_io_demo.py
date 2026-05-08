"""RAW I/O demo — wire 에 실제 가는 payload + 받는 raw response.

학습 원칙:
  매 LLM 호출마다 (1) 요청 payload 전체와 (2) 응답 객체 전체를
  요약·가공 없이 JSON 그대로 출력한다.

  이 파일은 가장 단순한 1-tool / 2-call 핑퐁만 보여주지만,
  print 되는 raw JSON 만 봐도 tool use 가 어떻게 돌아가는지 100% 추적 가능.
"""

import json
import sys

from anthropic import Anthropic
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()
client = Anthropic()


def _block_dict(b):
    return b if isinstance(b, dict) else b.model_dump()


def render_prompt(payload: dict) -> str:
    """모델이 실제로 보는 의미 콘텐츠만 사람 읽기 좋은 텍스트 흐름으로.

    JSON wrapper("role", "content", "messages" 등) 는 모델 prompt 에
    안 들어가니 view 에서도 뺀다. 학습용 main view.
    """
    out = []

    sys_text = payload.get("system")
    if sys_text:
        out.append("[SYSTEM]")
        out.append(sys_text if isinstance(sys_text, str) else json.dumps(sys_text, ensure_ascii=False))
        out.append("")

    tools = payload.get("tools")
    if tools:
        out.append("[TOOLS]")
        for t in tools:
            schema = t.get("input_schema", {})
            props = schema.get("properties", {})
            required = set(schema.get("required", []))
            sig = ", ".join(
                f"{n}{'?' if n not in required else ''}:{p.get('type','?')}"
                for n, p in props.items()
            )
            out.append(f"  - {t['name']}({sig})")
            out.append(f"      desc: {t['description']}")
            for n, p in props.items():
                pdesc = p.get("description", "")
                if pdesc:
                    out.append(f"      @{n}: {pdesc}")
        out.append("")

    msgs = payload.get("messages", [])
    if msgs:
        out.append("[MESSAGES]")
        for m in msgs:
            role = m["role"]
            content = m["content"]
            if isinstance(content, str):
                out.append(f"  {role:<9} : {content}")
                continue
            for block in content:
                bd = _block_dict(block)
                btype = bd.get("type")
                if btype == "text":
                    out.append(f"  {role:<9} : {bd.get('text', '')}")
                elif btype == "tool_use":
                    inp = json.dumps(bd.get("input", {}), ensure_ascii=False)
                    out.append(
                        f"  {role:<9} [tool_use id={bd.get('id')}]: "
                        f"{bd.get('name')}({inp})"
                    )
                elif btype == "tool_result":
                    out.append(
                        f"  {role:<9} [tool_result id={bd.get('tool_use_id')}]: "
                        f"{bd.get('content')}"
                    )
                else:
                    out.append(f"  {role:<9} [{btype}]: {bd}")
    return "\n".join(out)


def render_output(resp_content) -> str:
    """모델이 만든 의미 콘텐츠만 (content 블록에서 type 별로)."""
    out = ["[OUTPUT]"]
    for block in resp_content:
        bd = _block_dict(block)
        btype = bd.get("type")
        if btype == "text":
            out.append(f"  text     : {bd.get('text', '')}")
        elif btype == "tool_use":
            inp = json.dumps(bd.get("input", {}), ensure_ascii=False)
            out.append(
                f"  tool_use [id={bd.get('id')}]: "
                f"{bd.get('name')}({inp})"
            )
        else:
            out.append(f"  {btype}: {bd}")
    return "\n".join(out)


def section_tokens(model: str, payload: dict) -> dict:
    """payload 의 각 섹션이 차지하는 입력 토큰을 count_tokens API 로 측정.

    각 섹션 토큰 = (그 섹션만 포함한 호출의 count) - (최소 베이스라인 count).
    """
    minimal_msg = [{"role": "user", "content": "x"}]  # count_tokens 는 messages 필수
    base = client.messages.count_tokens(model=model, messages=minimal_msg).input_tokens

    out: dict = {}
    if payload.get("system"):
        v = client.messages.count_tokens(
            model=model, system=payload["system"], messages=minimal_msg
        ).input_tokens
        out["system"] = v - base
    if payload.get("tools"):
        v = client.messages.count_tokens(
            model=model, tools=payload["tools"], messages=minimal_msg
        ).input_tokens
        out["tools"] = v - base
    if payload.get("messages"):
        v = client.messages.count_tokens(
            model=model, messages=payload["messages"]
        ).input_tokens
        out["messages"] = v - base
    out["__base__"] = base
    return out


def call(label: str, payload: dict):
    """학습용 main: 섹션별 토큰 + PROMPT VIEW + OUTPUT."""
    print("\n" + "█" * 72)
    print(f" {label}")
    print("█" * 72)

    tokens = section_tokens(payload["model"], payload)

    # PROMPT VIEW with token annotations
    print("\n>>> 모델이 본 prompt  (섹션 옆 숫자는 그 섹션의 순 입력 토큰)\n")

    sys_text = payload.get("system")
    if sys_text:
        print(f"[SYSTEM]   ({tokens.get('system', 0)} 토큰)")
        print(f"  {sys_text if isinstance(sys_text, str) else json.dumps(sys_text, ensure_ascii=False)}\n")

    tools = payload.get("tools")
    if tools:
        print(f"[TOOLS]    ({tokens.get('tools', 0)} 토큰)")
        for t in tools:
            schema = t.get("input_schema", {})
            props = schema.get("properties", {})
            required = set(schema.get("required", []))
            sig = ", ".join(
                f"{n}{'?' if n not in required else ''}:{p.get('type','?')}"
                for n, p in props.items()
            )
            print(f"  - {t['name']}({sig})")
            print(f"      desc: {t['description']}")
            for n, p in props.items():
                pdesc = p.get("description", "")
                if pdesc:
                    print(f"      @{n}: {pdesc}")
        print()

    msgs = payload.get("messages", [])
    if msgs:
        print(f"[MESSAGES] ({tokens.get('messages', 0)} 토큰)")
        for m in msgs:
            role = m["role"]
            content = m["content"]
            if isinstance(content, str):
                print(f"  {role:<9} : {content}")
                continue
            for block in content:
                bd = _block_dict(block)
                btype = bd.get("type")
                if btype == "text":
                    print(f"  {role:<9} : {bd.get('text', '')}")
                elif btype == "tool_use":
                    inp = json.dumps(bd.get("input", {}), ensure_ascii=False)
                    print(f"  {role:<9} [tool_use id={bd.get('id')}]: {bd.get('name')}({inp})")
                elif btype == "tool_result":
                    print(
                        f"  {role:<9} [tool_result id={bd.get('tool_use_id')}]: "
                        f"{bd.get('content')}"
                    )

    # 실제 호출
    resp = client.messages.create(**payload)

    print(
        f"\n  ── 섹션 합계: {sum(v for k, v in tokens.items() if k != '__base__')} 토큰  "
        f"+ 베이스라인 {tokens['__base__']} 토큰  "
        f"≈ 실제 input_tokens={resp.usage.input_tokens}"
    )

    # OUTPUT
    print("\n<<< 모델이 만든 응답\n")
    for block in resp.content:
        bd = _block_dict(block)
        btype = bd.get("type")
        if btype == "text":
            print(f"  text     : {bd.get('text', '')}")
        elif btype == "tool_use":
            inp = json.dumps(bd.get("input", {}), ensure_ascii=False)
            print(f"  tool_use [id={bd.get('id')}]: {bd.get('name')}({inp})")
        else:
            print(f"  {btype}: {bd}")

    print(f"\n[meta] stop_reason={resp.stop_reason}")
    return resp


# ── 실행 ────────────────────────────────────────────────────────
if __name__ == "__main__":
    # ─────────────────────────────────────────────────────────────
    # 1차 호출 — user 메시지 1개만 보냄
    # ─────────────────────────────────────────────────────────────
    payload_1 = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 256,
        "tools": [
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
        ],
        "messages": [
            {"role": "user", "content": "서울 날씨 알려줘"}
        ],
    }
    resp_1 = call("CALL #1", payload_1)

    # ─────────────────────────────────────────────────────────────
    # 도구 실제 실행 (mock)
    # ─────────────────────────────────────────────────────────────
    tool_use_block = next(b for b in resp_1.content if b.type == "tool_use")
    tool_output = "맑음, 22°C, 풍속 약함"
    print("\n[LOCAL EXEC]")
    print(f"  function : get_weather")
    print(f"  arguments: {json.dumps(tool_use_block.input, ensure_ascii=False)}")
    print(f"  return   : {tool_output!r}")

    # ─────────────────────────────────────────────────────────────
    # 2차 호출 — 1차 응답을 messages 에 그대로 누적 + tool_result 회신
    # ─────────────────────────────────────────────────────────────
    payload_2 = {
        **payload_1,  # model · max_tokens · tools 그대로 재사용
        "messages": [
            *payload_1["messages"],
            # 1차 assistant 응답을 dict 로 변환해서 누적
            {
                "role": "assistant",
                "content": [b.model_dump() for b in resp_1.content],
            },
            # tool_result 회신
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": tool_output,
                    }
                ],
            },
        ],
    }
    resp_2 = call("CALL #2", payload_2)
