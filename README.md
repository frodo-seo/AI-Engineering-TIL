# AI Engineering Notes

AI를 "잘 쓰는" 엔지니어가 되기 위한 학습 저장소.
Context Engineering, RAG, Agent, MCP, Ontology, Harness Engineering까지.

## 커리큘럼

| Phase | 주제 | 폴더 |
|---|---|---|
| 0 | 기반 다지기 (LLM·API 감각) | `00_basics/` |
| 1 | Prompt & Context Engineering | `01_context_eng/` |
| 2 | Tool Use & 구조화 출력 | `02_tools/` |
| 3 | RAG 기초 → 심화 | `03_rag/` |
| 4 | Agent & LangGraph | `04_agents/` |
| 5 | MCP (Model Context Protocol) | `05_mcp/` |
| 6 | Ontology & GraphRAG | `06_ontology/` |
| 7 | Harness Engineering & 평가 | `07_harness/` |
| - | Capstone | `capstone/` |
| - | 읽은 자료 요약 | `notes/` |

## 셋업

```powershell
# 1) 가상환경 활성화
.venv\Scripts\Activate.ps1

# 2) 패키지 설치
pip install -r requirements.txt

# 3) API 키 설정
copy .env.example .env
# .env 파일을 열어 ANTHROPIC_API_KEY를 본인 키로 교체

# 4) 동작 확인
python 00_basics/setup_check.py
```

## 학습 규칙

- **하루 30분.** 넘기면 다음 날로 미룸.
- **산출물이 있다.** 코드든 노트든 뭔가 남긴다.
- **헷갈렸던 것을 기록한다.** 그게 복습 자료.
