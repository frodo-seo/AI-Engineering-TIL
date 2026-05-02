"""Day 3. Extended Thinking 비교

같은 질문을 thinking OFF / ON 두 번 호출해서 비교한다.
- 응답 블록 구조 (thinking 블록이 따로 붙는가)
- 토큰 사용량 (input / output)
- latency
- 답변 품질 차이
"""

import time

from dotenv import load_dotenv

from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# Sonnet 4.6 — extended thinking 지원 모델 중 가성비 기본값.
# Opus 4.7 로 바꿔서 비교해보면 thinking 의 효과가 더 잘 드러나는 task 도 있다.
MODEL = "claude-sonnet-4-5"
QUESTION = (
    "파이썬에서 리스트를 순회하며 동시에 수정하면 왜 위험한지 설명하고, "
    "안전한 방법 3가지를 비교해줘. 각 방법의 장단점도 같이."
)


def call(thinking: bool):
    kwargs = {
        "model": MODEL,
        "max_tokens": 4000,
        "messages": [{"role": "user", "content": QUESTION}],
    }
    if thinking:
        # budget_tokens: thinking 블록에 쓸 토큰 예산. 최소 1024, max_tokens 보다 작게.
        # 클수록 더 깊게 생각함. 너무 크면 latency·비용만 늘고 답은 그대로.
        kwargs["thinking"] = {"type": "enabled", "budget_tokens": 2000}

    t0 = time.perf_counter()
    resp = client.messages.create(**kwargs)
    return resp, time.perf_counter() - t0


def show(label: str, resp, elapsed: float) -> None:
    print(f"\n{'=' * 72}")
    print(f"[{label}]  latency={elapsed:.2f}s")
    print(
        f"usage: input={resp.usage.input_tokens}, "
        f"output={resp.usage.output_tokens}"
    )

    # extended thinking 응답은 content 안에 thinking 블록 + text 블록이 함께 들어온다.
    # OFF 일 땐 text 블록만.
    for i, block in enumerate(resp.content):
        if block.type == "thinking":
            print(f"\n--- block {i}: thinking ({len(block.thinking)} chars) ---")
            print(block.thinking)
        elif block.type == "text":
            print(f"\n--- block {i}: text ({len(block.text)} chars) ---")
            print(block.text)
        else:
            print(f"\n--- block {i}: {block.type} (skipped) ---")


if __name__ == "__main__":
    print("[1/2] thinking OFF ...")
    resp_off, t_off = call(thinking=False)
    show("OFF", resp_off, t_off)

    print("\n[2/2] thinking ON (budget=2000) ...")
    resp_on, t_on = call(thinking=True)
    show("ON", resp_on, t_on)

    print("\n" + "=" * 72)
    print("관찰 포인트")
    print(f"- latency:       OFF {t_off:.2f}s   vs   ON {t_on:.2f}s")
    print(
        f"- output tokens: OFF {resp_off.usage.output_tokens}   vs   "
        f"ON {resp_on.usage.output_tokens}"
    )
    print("- ON 응답에 thinking 블록이 따로 보이나? 길이는?")
    print("- ON 의 최종 text 답변이 OFF 보다 더 정확/체계적인가?")
    print("- 이 질문에서 thinking 켤 가치 있었나? (비용 vs 품질)")
