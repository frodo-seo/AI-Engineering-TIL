# AI Engineering Notes

AI를 "잘 쓰는" 엔지니어가 되기 위한 학습 저장소.
Context Engineering → Tools → RAG → Agents → MCP → GraphRAG 까지,
**오늘의 AI Engineering** 이 실제로 다루는 본질을 짧게·꾸준히 익힌다.

> **Harness 디자인 / Capstone / Production / Eval 심화** 는 별도 repo 에서 진행.

## 이 커리큘럼의 전제

- 기본(토큰·temperature·멀티턴·SDK 사용)은 이미 안다고 가정한다. `00_refresh/` 는 **최신 기능 훑기용 optional 폴더** (caching / thinking / batch / vision).
- "AI를 쓰는 앱"을 짜는 쪽에 집중한다. 모델을 **학습** 시키는 게 아니라 **조합·평가·배포** 한다.
- 기본 모델은 Claude 4.x (Opus 4.7 / Sonnet 4.6 / Haiku 4.5).

## 커리큘럼 한눈에

| Phase | 주제 | 폴더 |
|---|---|---|
| 0 | 최신 Claude 기능 refresh (**optional**) | `00_refresh/` |
| 1 | Context Engineering | `01_context_eng/` |
| 2 | Tool Use & Structured Output | `02_tools/` |
| 3 | RAG 심화 | `03_rag/` |
| 4 | Agents | `04_agents/` |
| 5 | MCP (Model Context Protocol) | `05_mcp/` |
| 6 | GraphRAG (**optional**, 도메인 의존) | `06_ontology/` |
| - | 읽은 자료 요약 | `notes/` |

## 진행 상황

| Phase | 상태 | 핵심으로 잡은 것 |
|---|---|---|
| 1. Context Engineering | 개념 ✓ | token · context window · message roles |
| 2. Tool Use & Structured Output | **개념 + 코드 ✓** | tool use = JSON 강제 + 외부 실행 + 결과 재투입 루프. structured output 은 그 특수 케이스. |
| 3. RAG 심화 | 개념 ✓ | 임베딩 (transformer + contrastive) · 청킹 · hybrid (BM25+vector) + RRF · reranker (cross-encoder) · prompt caching · Contextual Retrieval |
| 4. Agents | 개념 ✓ (`patterns.md`) | Anthropic 5 패턴 (chaining/routing/parallel/orchestrator/agent) · workflow vs agent 판단 · LangGraph 의 가치 · agent memory |
| 5. MCP | **개념 + 코드 ✓** | MCP = LLM 측 변화 0, 도구 패키징·배포 표준. host ↔ server (stdio/HTTP). LLM 은 MCP 모름 — host 가 다리. CLI vs MCP 의 실용적 균형. |
| 6. GraphRAG | **개념 + 코드 ✓** (`graphify_demo`) | Graph RAG 는 raw 청크 대신 **AST 가 뽑은 구조 사실** 을 LLM 에 보냄 → 80× 토큰 절감. 구조 query 영역 한정. |

## 참고 자료 (상시 열람)

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

```bash
# 1) 가상환경 (Windows)
.venv\Scripts\Activate.ps1

# 2) 패키지 설치
pip install -r requirements.txt

# 3) API 키
copy .env.example .env
# .env 에 ANTHROPIC_API_KEY 채우기

# 4) 동작 확인
python 00_refresh/setup_check.py
```
