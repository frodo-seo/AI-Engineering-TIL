# Phase 4. Agents

**한 줄**: LLM + 도구 + 루프, 단 LLM 이 "다음에 뭘 할지" 를 스스로 결정하는 시스템.

> **Agent 부터 의심하지 말고 chaining 부터 의심하라.** 가장 단순한 패턴으로 풀 수 있는지 위에서 아래로 검토.

## 잡은 핵심 개념

### Workflow vs Agent

| | Workflow | Agent |
|---|---|---|
| 흐름 결정 | 너 (코드로 미리 박음) | LLM (매 턴 결정) |
| 예측가능성 | 높음, 디버깅 쉬움 | 낮음, trace 봐야 알 수 있음 |
| 비용/latency | 결정적 | 가변적 (5~50번) |
| 실패 모드 | 예상 가능 | 무한루프, 도구 오용, 비용 폭발 |

→ **대부분의 task 는 agent 가 아니라 workflow.** agent 는 사전에 단계를 정할 수 없는 진짜 동적 task 의 마지막 카드.

### 5 패턴 (자세한 건 `patterns.md`)

1. **Prompt Chaining** — 직선 파이프라인
2. **Routing** — 분기 라우팅
3. **Parallelization** — sectioning (독립 부분) / voting (합의)
4. **Orchestrator-Worker** — 중앙 조정자가 동적 위임
5. **Autonomous Agent** — 자율 루프 (`while`)

위에서 아래로 자율성 ↑, 통제력 ↓.

### LangGraph 의 가치

- raw API 로 단순 ReAct 는 30줄. 근데 **state 관리 / 재개 (checkpointer) / HITL / streaming / multi-agent** 가 들어가면 raw 는 수백 줄, LangGraph 는 한 줄짜리 옵션.
- 가치는 **"agent 를 그래프 (node + edge + state) 로 표현"** + 5대 production 요건의 framework 처리.
- 단순 case 는 raw 가 짧음. production 가까워질수록 LangGraph 가 절감.
- 대안: Anthropic Agent SDK / CrewAI / AutoGen / DSPy. LangGraph 가 현재 보편 표준에 가까움.

### Agent Memory

- **단기**: 현재 진행 중인 task 의 messages 배열. context window 한계 → sliding window / summarization.
- **장기**: 세션 넘어 살아남는 기억. RAG-on-self.
  - **Semantic** (선호·사실, vector DB)
  - **Episodic** (과거 사건, log)
  - **Procedural** (how-to, prompt 템플릿)
- 4대 어려움: **Write 결정 / Read 시점 / Staleness / Memory pollution**.
- 도구: Mem0, Graphiti (temporal KG), Letta, LangMem, Zep.
- MCP 와 연결: memory 를 MCP 서버로 노출하면 여러 agent 가 공유 가능.

## 폴더 내용

- `patterns.md` — 5 패턴 + 패턴별 프로젝트 후보 (OCR / 라우터 / PR 리뷰 / 여행 / 코딩 agent)

## 참고

- **Anthropic: "Building effective agents"** (2024.12) — phase 의 뼈대
- Lilian Weng: "LLM Powered Autonomous Agents"
- Harrison Chase: LangGraph 시리즈 + "Context engineering for agents"
- docs: langchain-ai.github.io/langgraph
