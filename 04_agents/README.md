# Phase 4. Agents

**목표**: "LLM + 루프 + 툴" 을 왜 Agent 라 부르는지, 그리고
**언제 agent 가 아니라 workflow 를 써야 하는지** 를 안다.
Anthropic "Building effective agents" 의 5가지 패턴을 축으로 직접 구현·비교한 뒤,
**Raw 구현의 한계 → LangGraph 가 메우는 지점** 을 손으로 체감한다.

**기간**: 30분 × 19일

## 학습 흐름

```
Raw API 로 패턴/에이전트 직접 구현 (Day 1~8)
        ↓ "상태·재개·HITL·스트리밍 직접 짜기 귀찮다" 체감
LangGraph 로 같은 걸 재작성 + 고급 기능 (Day 9~14)
        ↓
Agent SDK 비교 → memory / planning / eval 로 마무리 (Day 15~19)
```

## Day-by-Day

| Day | 주제 | 산출물 |
|---|---|---|
| 1 | 읽기: **Anthropic "Building effective agents" (2024.12)** | `../notes/p4_day01.md` 정독 요약 |
| 2 | Workflow vs Agent — 언제 어느 쪽? 판단 기준 | `when_to_use.md` |
| 3 | Pattern 1: Prompt chaining | `p1_chaining.py` |
| 4 | Pattern 2: Routing | `p2_routing.py` |
| 5 | Pattern 3: Parallelization (sectioning + voting) | `p3_parallel.py` |
| 6 | Pattern 4: Orchestrator-worker | `p4_orchestrator.py` |
| 7 | Pattern 5: Evaluator-optimizer | `p5_evaluator.py` |
| 8 | ReAct loop 를 raw 로 직접 구현 (프레임워크 없이) | `react_raw.py` |
| 9 | **LangGraph 입문**: StateGraph / Node / Edge / State 개념 | `lg01_basics.py` + `lg_notes.md` |
| 10 | **LangGraph ReAct**: Day 8 raw → LangGraph 로 재작성, 코드 비교 | `lg02_react.py` + 비교 노트 |
| 11 | **LangGraph Checkpointer**: thread 별 상태, 크래시 후 재개 | `lg03_checkpoint.py` |
| 12 | **LangGraph Human-in-the-loop**: `interrupt()` 로 승인 흐름 | `lg04_hitl.py` |
| 13 | **LangGraph Streaming**: `.stream()` 모드별 (values/updates/messages) | `lg05_streaming.py` |
| 14 | **LangGraph 멀티 에이전트**: supervisor + worker 패턴 | `lg06_multiagent.py` |
| 15 | Claude Agent SDK 소개 & LangGraph 와 비교 — 언제 무엇? | `agent_sdk_note.md` |
| 16 | Agent memory: short-term (message window) · long-term (vector) | `memory_agent.py` |
| 17 | Planning vs reactive — "plan-and-execute" 패턴 | `plan_execute.py` |
| 18 | Agent 평가: trajectory eval · final-state eval | `agent_eval.py` |
| 19 | 회고 + mini-project 구상 | README 하단 |

## 참고 (필수)

- **Anthropic: "Building effective agents"** — 이 Phase 의 뼈대
- **Lilian Weng**: "LLM Powered Autonomous Agents"
- **Harrison Chase YouTube**: LangGraph 시리즈 + "Context engineering for agents"
- **LangChain blog**: agent 아키텍처 글 전부
- **AI Engineer Summit**: agent 트랙
- **Sam Witteveen**, **Matthew Berman**: 튜토리얼
- docs: langchain-ai.github.io/langgraph
- **TeddyNote `langgraph` repo** — 한국어 LangGraph 실습 (참고용, 로컬에서만)

## 끝났을 때 할 줄 아는 것

- "이건 agent 가 아니라 workflow 로 해야 한다" 를 자신 있게 말한다.
- 5 패턴 중 상황에 맞는 걸 고른다.
- LangGraph 로 상태 있는 agent 를 짠다 — checkpointer, HITL, streaming, multi-agent.
- "LangGraph 가 raw API 대비 뭘 줘서 시간을 절약하는지" 를 코드로 설명한다.
- agent 의 trajectory 를 평가한다.

## 회고

- 배운 것 5개:
- 헷갈린 것 3개:
- 다음에 궁금한 것 3개:
