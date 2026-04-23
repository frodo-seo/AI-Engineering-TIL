# Phase 4. Agents

**목표**: "LLM + 루프 + 툴" 을 왜 Agent 라 부르는지, 그리고
**언제 agent 가 아니라 workflow 를 써야 하는지** 를 안다.
Anthropic "Building effective agents" 의 5가지 패턴을 축으로 직접 구현·비교.

**기간**: 30분 × 15일

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
| 9 | LangGraph 기초 — StateGraph 로 재작성 | `langgraph_agent.py` |
| 10 | Claude Agent SDK 소개 & LangGraph 와 비교 | `agent_sdk_note.md` |
| 11 | Agent memory: short-term (message window) · long-term (vector) | `memory_agent.py` |
| 12 | Planning vs reactive — "plan-and-execute" 패턴 | `plan_execute.py` |
| 13 | Human-in-the-loop (approval / edit) | `hitl_agent.py` |
| 14 | Agent 평가: trajectory eval · final-state eval | `agent_eval.py` |
| 15 | 회고 + mini-project 구상 | README 하단 |

## 참고 (필수)

- **Anthropic: "Building effective agents"** — 이 Phase 의 뼈대
- **Lilian Weng**: "LLM Powered Autonomous Agents"
- **Harrison Chase YouTube**: LangGraph 시리즈 + "Context engineering for agents"
- **LangChain blog**: agent 아키텍처 글 전부
- **AI Engineer Summit**: agent 트랙
- **Sam Witteveen**, **Matthew Berman**: 튜토리얼
- docs: langchain-ai.github.io/langgraph

## 끝났을 때 할 줄 아는 것

- "이건 agent 가 아니라 workflow 로 해야 한다" 를 자신 있게 말한다.
- 5 패턴 중 상황에 맞는 걸 고른다.
- LangGraph 로 상태 있는 agent 를 짠다.
- agent 의 trajectory 를 평가한다.

## 회고

- 배운 것 5개:
- 헷갈린 것 3개:
- 다음에 궁금한 것 3개:
