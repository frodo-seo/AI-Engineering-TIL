# Phase 2. Tool Use & Structured Output

**목표**: LLM 을 "답 생성기" 에서 "행동하는 컴포넌트" 로 바꾸는 지점.
툴을 **정의·호출·체이닝·에러처리** 하고, 출력을 **타입 검증 가능한 객체** 로 받는다.

**기간**: 30분 × 10일

## Day-by-Day

| Day | 주제 | 산출물 |
|---|---|---|
| 1 | Tool use 기본 API (tool 정의 · `tool_use` / `tool_result` 메시지 흐름) | `tool_basic.py` |
| 2 | 좋은 tool 설계 원칙 (이름·description·input_schema·에러 메시지) | `tool_design.md` |
| 3 | Parallel tool use — 한 턴에 여러 툴 | `parallel_tools.py` |
| 4 | Tool chain — 툴 결과 → 다음 툴 인자 | `tool_chain.py` (예: 검색 → 선택 → 예약) |
| 5 | Pydantic + JSON schema 로 출력 강제 | `pydantic_output.py` |
| 6 | Instructor 라이브러리 — 실전 패턴 | `instructor_demo.py` |
| 7 | 구조화 추출: 뉴스 기사 → `Article` 객체 | `article_extract.py` |
| 8 | 에러 · 재시도 · validation loop | `tool_retry.py` |
| 9 | Computer use / bash tool 개념 체험 | `computer_use_note.md` |
| 10 | Mini-project: "CSV 1줄 → 정규화된 객체" 추출기 | `mini_extractor/` |

## 참고

- **Anthropic Docs**: "Tool use", "Computer use"
- **Jason Liu**: Instructor 블로그 + YouTube "Pydantic is all you need"
- **Hamel Husain**: tool-calling 평가 글
- LangChain blog: structured output 패턴
- YouTube: AI Engineer Summit — structured output 세션

## 끝났을 때 할 줄 아는 것

- 여러 툴을 체이닝해 하나의 태스크를 완수시킨다.
- LLM 출력을 dict 가 아닌 Pydantic 모델로 받는다.
- 툴 호출 실패 시 재시도·수정 루프를 만든다.
- "이건 tool 로 풀지 structured output 으로 풀지" 를 구분한다.

## 회고

- 배운 것 5개:
- 헷갈린 것 3개:
- 다음에 궁금한 것 3개:
