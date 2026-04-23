# Phase 7. Evals & Observability

**목표**: "LLM 앱이 잘 동작하는가?" 에 **숫자로** 답할 수 있게 된다.
느낌으로 튜닝하던 걸 끝낸다. "vibes-based" 에서 벗어나는 단계.

**기간**: 30분 × 10일

## Day-by-Day

| Day | 주제 | 산출물 |
|---|---|---|
| 1 | 읽기: **Hamel Husain "Your AI Product Needs Evals"** | `why_evals.md` 요약 |
| 2 | Golden dataset 만들기 (실사용 30개) | `eval/golden.jsonl` |
| 3 | 코드 기반 assertion: 정확 일치 · 포맷 · 길이 · 정규식 | `assertions.py` |
| 4 | LLM-as-judge 기초 · 함정 (bias / position / verbosity / self-preference) | `judge_basic.py` |
| 5 | Judge 개선: rubric · pairwise · few-shot calibration | `judge_v2.py` |
| 6 | Langfuse (또는 Braintrust · Phoenix) 로 trace 기록 | `obs_setup.md` |
| 7 | Online vs Offline eval — 역할 구분 | `eval_note.md` |
| 8 | Regression 파이프라인 (pytest + eval) | `tests/test_regression.py` |
| 9 | 비용·지연 추적 & A/B 프레임워크 | `ab_framework.py` |
| 10 | Mini-project: Phase 3 RAG 에 평가·관측 붙이기 | `report.md` |

## 참고 (필수)

- **Hamel Husain**: "Your AI Product Needs Evals" — 이 Phase 의 성경
- **Eugene Yan**: "Evaluating LLM Applications"
- **Shreya Shankar**: eval 관련 논문/블로그 (DocETL 등)
- Chip Huyen *AI Engineering* 3~4장
- **Langfuse / Braintrust / Phoenix (Arize)** docs
- **YouTube**: AI Engineer Summit eval 트랙 (Hamel, Shreya, Eugene 발표 전부)
- OpenAI Evals 레포 / Anthropic eval cookbook

## 끝났을 때 할 줄 아는 것

- "이 변경이 성능을 좋게 했나?" 를 숫자로 답한다.
- LLM-judge 를 만들되 그 함정을 안다.
- 프로덕션 트래픽에서 online eval 을 돌린다.
- CI 에 regression 테스트를 건다.

## 회고

- 배운 것 5개:
- 헷갈린 것 3개:
- 다음에 궁금한 것 3개:
