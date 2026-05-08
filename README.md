# AI Engineering Notes

LLM 앱을 짜는 데 필요한 본질 개념을 짧게·꾸준히 익히는 저장소.
**Tools → RAG → Agents → MCP**.

> **Harness 디자인 / Capstone / Production / Eval 심화** 는 별도 repo 에서 진행.

## 진행 상황

| Phase | 폴더 | 상태 | 핵심으로 잡은 것 |
|---|---|---|---|
| 2. Tool Use & Structured Output | `02_tools/` | **개념 + 코드 ✓** | tool use = JSON 강제 + 외부 실행 + 결과 재투입 루프. structured output 은 그 특수 케이스. |
| 3. RAG 심화 | `03_rag/` | 개념 ✓ | 임베딩 (transformer + contrastive) · 청킹 · hybrid (BM25+vector) + RRF · reranker (cross-encoder) · prompt caching · Contextual Retrieval |
| 4. Agents | `04_agents/` | 개념 ✓ (`patterns.md`) | Anthropic 5 패턴 (chaining/routing/parallel/orchestrator/agent) · workflow vs agent 판단 · LangGraph 의 가치 · agent memory |
| 5. MCP | `05_mcp/` | **개념 + 코드 ✓** | MCP = LLM 측 변화 0, 도구 패키징·배포 표준. host ↔ server (stdio/HTTP). LLM 은 MCP 모름 — host 가 다리. CLI vs MCP 의 실용적 균형. |

## 참고 자료

### 책
- Chip Huyen, *AI Engineering* (O'Reilly, 2024)
- Jay Alammar, *Hands-On LLMs*

### 블로그
- **Anthropic**: "Building effective agents", "Contextual Retrieval", "Prompt caching", "Code execution with MCP"
- **Lilian Weng**: "LLM Powered Autonomous Agents"
- **Eugene Yan**, **Simon Willison**, **Harrison Chase**, **Jason Liu**, **Hamel Husain**

### 유튜브
- **Andrej Karpathy**, **DeepLearning.AI**, **LangChain**, **AI Engineer Summit**, **Greg Kamradt**

### Docs
- docs.anthropic.com
- modelcontextprotocol.io
- langchain-ai.github.io/langgraph

## 셋업

```powershell
# 1) 가상환경 (Windows)
.venv\Scripts\Activate.ps1

# 2) 패키지 설치
pip install -r requirements.txt

# 3) API 키
copy .env.example .env
# .env 에 ANTHROPIC_API_KEY 채우기
```
