# Phase 1. Context Engineering

**한 줄**: 200K 토큰의 한정된 작업대를 무엇으로·어떤 순서로·얼마만큼 채울지의 설계 학문.

> "prompt engineering is a subset of context engineering."

## 잡은 핵심 개념

- **토큰** — LLM 이 단어가 아니라 토큰 단위로 읽고 씀. 한국어는 영어보다 토큰·비용이 더 든다.
- **컨텍스트 윈도우** — 모델이 한 번에 볼 수 있는 토큰 총량 (input + output). Claude 200K 안에 시스템 프롬프트, 대화, 문서, 응답이 모두 들어가야.
- **메시지 역할** — `system` (정체성·규칙), `user` (입력), `assistant` (출력). 멀티턴은 과거 assistant 답변도 누적.
- **Prompt caching** — prefix 가 결정적이고 재사용되면 cache write (1.25x) 후 cache read (0.1x). 적중률 낮으면 손해. 자세한 내용은 Phase 3 쪽에서 같이 다룸.

## 참고

- Anthropic: "Long context prompting tips", "Contextual Retrieval" (2024.09)
- Karpathy: "context engineering" 글타래
- Harrison Chase: "Context engineering" 블로그
- Greg Kamradt: needle-in-haystack 영상
- Chip Huyen *AI Engineering* 5장
