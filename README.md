# AI Engineering Notes

AI를 "잘 쓰는" 엔지니어가 되기 위한 학습 저장소.
Context Engineering → Tools → RAG → Agents → MCP → Ontology → Evals → Production 까지,
**오늘의 AI Engineering** 이 실제로 다루는 것들을 짧게·꾸준히 익힌다.

## 이 커리큘럼의 전제

- 기본(토큰·temperature·멀티턴·SDK 사용)은 이미 안다고 가정한다. `00_refresh/` 는 **최신 기능 훑기용 optional 폴더** (caching / thinking / batch / vision).
- "AI를 쓰는 앱"을 짜는 쪽에 집중한다. 모델을 **학습** 시키는 게 아니라 **조합·평가·배포** 한다.
- 기본 모델은 Claude 4.x (Opus 4.7 / Sonnet 4.6 / Haiku 4.5). 필요할 때만 다른 모델 비교.

## 커리큘럼 한눈에

| Phase | 주제 | 폴더 | 기간(30분/일) |
|---|---|---|---|
| 0 | 최신 Claude 기능 refresh (**optional**) | `00_refresh/` | 5일 |
| 1 | Context Engineering | `01_context_eng/` | 10일 |
| 2 | Tool Use & Structured Output | `02_tools/` | 10일 |
| 3 | RAG 심화 | `03_rag/` | 15일 |
| 4 | Agents | `04_agents/` | 15일 |
| 5 | MCP (Model Context Protocol) | `05_mcp/` | 10일 |
| 6 | Ontology & GraphRAG | `06_ontology/` | 10일 |
| 7 | Evals & Observability | `07_harness/` | 10일 |
| 8 | Production (보안·비용·배포) | `08_production/` | 10일 |
| - | Capstone (통합 프로젝트) | `capstone/` | 30일 |
| - | 읽은 자료 요약 | `notes/` | 수시 |

총 약 **115일 ≈ 4~5개월**. 30분/일 기준. (Phase 0 skip 시 110일)

## 학습 규칙

- **하루 30분.** 넘기면 다음 날로. 꾸준함 > 깊이.
- **산출물이 있다.** 각 Day 에 코드든 노트든 뭔가 남긴다.
- **헷갈린 걸 기록한다.** `notes/dayNN.md`. 그게 복습 자료.
- **Phase 끝마다 회고.** 배운 거 5 / 헷갈린 거 3 / 다음 궁금한 거 3.
- **평가셋이 먼저.** RAG·Agent 단계부터는 golden set 없으면 개선 여부를 모른다.

## 참고 자료 (상시 열람)

### 책
- Chip Huyen, *AI Engineering* (O'Reilly, 2024) — 전체 커리큘럼의 뼈대
- Jay Alammar, *Hands-On LLMs*

### 블로그
- **Anthropic**: "Building effective agents", "Contextual Retrieval", "Prompt caching", "Code execution with MCP"
- **Lilian Weng**: "LLM Powered Autonomous Agents", "Prompt Engineering"
- **Eugene Yan**: patterns, evals, RAG
- **Simon Willison**: 매일 업데이트되는 AI 링크 큐레이션 + prompt injection 시리즈
- **Harrison Chase (LangChain)**: context engineering, agents
- **Jason Liu**: Instructor, RAG 레벨링
- **Hamel Husain**: "Your AI Product Needs Evals"

### 유튜브
- **Andrej Karpathy** — "Intro to LLMs", "Let's build GPT", "Software 3.0"
- **DeepLearning.AI short courses** (Andrew Ng)
- **LangChain** — agent·RAG 실전 (Lance Martin, Harrison Chase)
- **AI Engineer Summit** — eval, agent, RAG 트랙
- **Greg Kamradt** — needle-in-haystack, long context
- **Sam Witteveen**, **Matthew Berman** — 튜토리얼

### Docs
- docs.anthropic.com
- modelcontextprotocol.io
- langchain-ai.github.io/langgraph

## 셋업

```bash
# 1) 가상환경 (Windows)
.venv\Scripts\Activate.ps1

# 2) 패키지 설치 (Phase 마다 필요한 것 추가)
pip install -r requirements.txt

# 3) API 키
copy .env.example .env
# .env 에 ANTHROPIC_API_KEY 채우기

# 4) 동작 확인 (Phase 0 설치·키 점검 스크립트)
python 00_refresh/setup_check.py
```

각 Phase 폴더에 들어가면 Day-by-Day 계획, 참고자료, 산출물 체크리스트가 있다.
**지금 당장 할 일은: `01_context_eng/README.md` 열기.**
