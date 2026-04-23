# Capstone — 내 것을 짓는다

**목표**: Phase 1~8 에서 배운 것을 **하나의 동작하는 앱** 으로 묶는다.
회사에서 "왜 LLM 앱이 이렇게 안 나오나요?" 물었을 때 보여줄 수 있는 한 덩어리.

**기간**: 30분 × 30일 (약 6주)

## 주제 선택지 (하나 고르고 스펙 잠그기)

1. **"내 문서 비서"** — 내 Obsidian / Google Drive 에 agentic RAG. MCP 서버로 노출. 인용 필수.
2. **"코드 리뷰 agent"** — PR 받아 evaluator-optimizer 루프로 리뷰. LangGraph.
3. **"연구 assistant"** — 웹 검색 + 요약 + 지식그래프 축적. deep-research 스타일.
4. **자유 주제** — 본인 업무·취미 기반. 단, Phase 1 · 2 · 3 · 4 · 7 중 **최소 4개** 를 쓸 것.

## 마일스톤

| 주차 | 단계 | 산출물 |
|---|---|---|
| Week 1 | **스펙 · 평가셋 먼저 (!)** | `spec.md` + `eval/golden.jsonl` 20~30개 |
| Week 2 | v0 — 부끄러울 정도로 단순한 파이프라인 | 동작하는 CLI · 첫 eval 리포트 |
| Week 3 | 개선 — RAG / agent / tool 중 핵심 1~2개 | 성능 변화 수치 보고 |
| Week 4 | 관측성 (Phase 7) 붙이기 | Langfuse trace · cost dashboard |
| Week 5 | 프로덕션 걱정 (Phase 8) — 보안 · guardrail · fallback | `hardening.md` |
| Week 6 | 배포 + 데모 영상 + 회고 | 공개 링크 · postmortem |

## 원칙

- **평가셋을 코드보다 먼저.** 없으면 개선했는지 모른다.
- **v0 는 부끄러울 정도로 단순하게.** 베이스라인이 있어야 비교가 된다.
- **숫자 없는 개선 주장 금지.** Phase 7 대로 regression 돌린다.
- **헛수고도 기록.** 뭘 시도해서 왜 안 됐는지가 다음 프로젝트의 자산.

## 회고 (Week 6)

- 처음 스펙 대비 실제로 만든 것:
- 가장 크게 바뀐 판단 3개:
- 다음 프로젝트로 가져갈 교훈 3개:
