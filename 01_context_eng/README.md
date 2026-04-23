# Phase 1. Context Engineering

**목표**: "프롬프트 쓰는 사람" → "컨텍스트를 설계하는 사람".
200K 토큰이라는 **한정된 작업대** 를 무엇으로·어떤 순서로·얼마만큼 채울지 감각을 만든다.

**기간**: 30분 × 10일

## 왜 "Prompt" 가 아니라 "Context" 인가

- 2024~25년 사이 Karpathy, Harrison Chase 등이 명시적으로 프레이밍을 전환했다.
- 단일 프롬프트 최적화가 아니라
  **시스템 프롬프트 + 툴 정의 + 검색 결과 + 메모리 + 예시 + 질문** 이 합쳐진
  "컨텍스트 전체" 의 설계가 성능을 결정한다.
- "prompt engineering is a subset of context engineering."

## Day-by-Day

| Day | 주제 | 산출물 |
|---|---|---|
| 1 | 읽기: Karpathy "context engineering" 글 + Anthropic "Long context tips" | `../notes/p1_day01.md` — 3줄 요약 |
| 2 | XML 구조화 패턴 (`<instructions>`, `<context>`, `<example>`) 체득 | `xml_structure.md` — 같은 task 3가지 구조로 비교 |
| 3 | System prompt 설계 5원칙 (역할·제약·출력형식·예외·톤) | `system_prompt_principles.md` |
| 4 | Few-shot: 개수·순서·위치에 따른 성능 차이 | `fewshot_experiment.py` (0 / 1 / 3 / 5 shot) |
| 5 | Context rot · "lost in the middle" 재현 | `context_rot.py` + 관찰 노트 |
| 6 | Prompt caching 전략: static prefix + dynamic tail 계층화 | `caching_strategy.py` — 비용 절감 수치 |
| 7 | 컨텍스트 예산: 20K vs 100K vs 200K 동일 task 비교 | `budget_bench.md` |
| 8 | Long-context 디버깅: needle-in-haystack 직접 돌리기 | `niah_eval.py` |
| 9 | Anthropic "Contextual Retrieval" 블로그 정독 | `contextual_retrieval.md` — 요약 + 내 태스크 적용 아이디어 |
| 10 | 회고 + Phase 2 전 미니 체크리스트 | README 하단 회고 섹션 |

## 참고

- **Anthropic blog**: "Long context prompting tips", "Contextual Retrieval" (2024.09)
- **Karpathy**: X/twitter 의 "context engineering" 글타래
- **Harrison Chase (LangChain)**: "Context engineering" 블로그 + YouTube
- **Greg Kamradt**: needle-in-haystack 영상
- **YouTube**: AI Engineer Summit 2024 — context engineering 세션
- Chip Huyen *AI Engineering* 5장

## 끝났을 때 할 줄 아는 것

- 새 태스크를 받으면 "컨텍스트에 뭐가 들어가야 하고, 뭘 캐시하고, 뭘 빼는지" 순서를 잡는다.
- `<xml>` 구조로 프롬프트를 조립한다.
- Prompt caching 으로 반복 비용을 크게 줄인다.
- context rot 의 징후를 알아본다.

## 회고 (Day 10)

- 배운 것 5개:
- 헷갈린 것 3개:
- 다음에 궁금한 것 3개:
