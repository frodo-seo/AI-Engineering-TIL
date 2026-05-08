# Pattern Capstones — 5 패턴, 5개의 portfolio

**목표**: Anthropic "Building effective agents" 의 **5가지 패턴** 마다 한 개씩, 총 5개의 동작하는 프로젝트를 짓는다.
Phase 1~8 에서 배운 무기 (context engineering · tools · RAG · agents · MCP · eval · production) 를
**5번 반복 적용** 하면서 portfolio 5개가 손에 남는 구조.

> 패턴 개념·예시는 [`../04_agents/patterns.md`](../04_agents/patterns.md) 참고.

**기간**: 30분 × 6일 × 5 패턴 = **30일** (약 6주)
**전제**: Phase 1~8 모두 통과한 후 시작.

---

## 진행 순서

```
Pattern 1 (Chaining)        → Day 1~6
Pattern 2 (Routing)         → Day 7~12
Pattern 3 (Parallel)        → Day 13~18
Pattern 4 (Orchestrator)    → Day 19~24
Pattern 5 (Agent)           → Day 25~30
```

위에서 아래로 갈수록 자율성·복잡도 ↑. 단순한 것부터 짠 다음 점점 통제 풀어가는 학습 곡선.

---

## 한 패턴당 6일 템플릿

| Day | 단계 | 산출물 |
|---|---|---|
| 1 | **스펙 + 평가셋** — 문제·범위·데이터·성공기준·golden 30개 | `spec.md` + `eval/golden.jsonl` |
| 2 | **v0 베이스라인** — 부끄러울 정도로 단순한 첫 동작 | 동작하는 코드 + 첫 eval 점수 |
| 3 | **코어 강화** — 패턴에 맞는 핵심 기법 적용 (RAG, MCP, 도구 등) | 점수 비교 |
| 4 | **Eval 강화 + 가드** — judge 추가, 실패 케이스 분석, 가드/fallback | regression 리포트 |
| 5 | **Production 적용** — 캐싱·배치·관측·비용·보안 (Phase 7-8) | `hardening.md` + 비용 측정 |
| 6 | **회고 + 데모** — postmortem, 다음 패턴 준비 | `report.md` + 데모 영상/스샷 |

---

## 5 패턴별 프로젝트

각 패턴마다 후보 3개. 진행 시 **본인 업무·관심 가까운 것** 으로 골라.

### Pattern 1. Chaining — 직선 파이프라인

| 후보 | 설명 |
|---|---|
| **OCR 영수증 처리** | 이미지 → OCR → 필드추출 → 검증 → DB. 본인 OCR 프로젝트 확장 가능 |
| 회의록 자동화 | 음성 → STT → 요약 → 액션아이템 → Slack |
| 블로그 자동화 | 주제 → 개요 → 본문 → SEO 메타 |

**적용 무기**: prompt caching · structured output · code-based eval · batch API

### Pattern 2. Routing — 분기 라우팅

| 후보 | 설명 |
|---|---|
| 고객지원 트리아지 | 분류 → FAQ(Haiku) / 환불(Sonnet) / 기술(Opus+도구) / 사람 |
| 코드 어시스턴트 | 자동완성(Haiku) / 리팩터링(Sonnet) / 설계(Opus) |
| 다국어 봇 | 언어 감지 → 언어별 특화 처리 |

**적용 무기**: 분류기 평가셋 · 비용 모델별 측정 · 라우팅 정확도 모니터링

### Pattern 3. Parallel — 병렬 (sectioning / voting)

| 후보 | 설명 |
|---|---|
| **PR 코드리뷰 봇** | 변경사항 → 보안/성능/스타일/테스트 동시 검토 → 통합 |
| 이력서 평가 | 기술/경력/문화핏/커뮤니케이션 동시 채점 |
| LLM-judge 안정화 | 같은 답변 N번 채점 → 평균/합의 |

**적용 무기**: 비동기 호출 · voting 으로 judge 노이즈 잡기 · 비용 N배 통제

### Pattern 4. Orchestrator-Worker — 동적 위임

| 후보 | 설명 |
|---|---|
| **여행 일정 생성기** | 항공/호텔/식당/박물관 worker 동시 + 동선 worker 추가 호출 |
| 리서치 어시스턴트 | 질문 분해 → 부분 검색·요약 → 통합 보고서 |
| 데이터 분석 봇 | SQL/차트/요약 worker 분담 → 보고서 |

**적용 무기**: MCP 서버를 worker 로 · max_iterations 가드 · trajectory eval

### Pattern 5. Autonomous Agent — 자율 루프

| 후보 | 설명 |
|---|---|
| 코딩/디버깅 agent | 에러 → 파일 탐색 → 가설 → 수정 → 재테스트 자율 |
| 이메일 자동화 | 받은편지함 → 분류 → 답장 → 일정 등록 |
| **DevOps incident response** | 알람 → 로그 검색 → 가설 → 수정 또는 인간 호출 |

**적용 무기**: LangGraph (checkpoint, HITL, streaming) · MCP 도구 · trajectory eval · 비용 한도 가드 · trace 관측

---

## 원칙

- **평가셋이 코드보다 먼저.** golden set 없으면 개선됐는지 모른다.
- **v0 는 부끄러울 정도로 단순하게.** 베이스라인이 있어야 비교가 된다.
- **숫자 없는 개선 주장 금지.** 매 변경마다 regression eval.
- **헛수고도 기록.** 시도하고 안 된 것이 다음 프로젝트의 자산.
- **5번 반복하면서 자기 패턴이 보일 것.** 어떤 단계가 매번 시간 잡아먹는지 → 본인 templating 이 만들어짐.

---

## 끝났을 때 (Day 30)

- portfolio 5개 (각 패턴별 동작 + eval 리포트 + 데모)
- "어떤 task 가 어느 패턴에 맞는지" 손에 박힘
- 본인의 LLM 앱 개발 template (스펙 → eval → v0 → 강화 → production) 굳음
- 회사에서 "이런 것도 만들 수 있냐" 물을 때 5개 중 가까운 걸로 즉답

## 회고 (전체 끝나고)

- 5 패턴 중 가장 어려웠던 것:
- 5 패턴 중 가장 자주 쓰일 것 같은 것:
- 5번 반복하면서 발견한 본인 패턴:
- Phase 1~8 무기 중 가장 큰 효과를 본 것:
- 다음 프로젝트로 가져갈 교훈 3개:
