# Phase 8. Production

**목표**: "데모는 되는데 배포가 겁나는" 단계를 넘는다.
보안 · 비용 · 배포 · 장애대응 — LLM 앱의 운영 현실.

**기간**: 30분 × 10일

## Day-by-Day

| Day | 주제 | 산출물 |
|---|---|---|
| 1 | OWASP "Top 10 for LLM Applications" 2025 판 훑기 | `owasp_llm.md` |
| 2 | Prompt injection 재현 & 방어 패턴 | `injection_lab.py` |
| 3 | PII · 기밀 데이터 마스킹 / redact 파이프라인 | `pii_pipeline.py` |
| 4 | Guardrails AI · NeMo Guardrails 비교 | `guardrails_demo.py` |
| 5 | Rate limit · retry · exponential backoff · 타임아웃 | `resilience.py` |
| 6 | 비용 최적화: 모델 라우팅 · caching · prompt compression | `cost_optim.md` |
| 7 | 스트리밍 UX — SSE · 토큰 단위 렌더 · 취소 | `streaming_ui.py` |
| 8 | 배포 옵션 비교: Vercel / Modal / Cloudflare / AWS Bedrock | `deploy_options.md` |
| 9 | 장애 플레이북 · fallback 모델 · graceful degradation | `incident_playbook.md` |
| 10 | 회고 + Capstone 킥오프 | README 하단 |

## 참고

- **OWASP**: "Top 10 for LLM Applications" (2025 개정)
- **Anthropic**: prompt injection defense 가이드, "Responsible scaling" 문서
- **Simon Willison**: prompt injection 시리즈 — 이 용어를 만든 사람
- **Vercel AI SDK docs**: streaming UX 패턴
- Chip Huyen *AI Engineering* 9~10장
- YouTube: AI Engineer Summit production 트랙

## 끝났을 때 할 줄 아는 것

- prompt injection 시나리오에서 뭐가 막히고 뭐가 뚫리는지 안다.
- 동일 요청을 Haiku/Sonnet/Opus 중 어디로 보낼지 라우팅 규칙을 짠다.
- 장애 시 대응 순서 · fallback 전략을 설명한다.
- 배포 플랫폼 선택을 근거를 가지고 한다.

## 회고

- 배운 것 5개:
- 헷갈린 것 3개:
- 다음에 궁금한 것 3개:
