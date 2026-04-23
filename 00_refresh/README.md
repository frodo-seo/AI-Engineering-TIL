# Phase 0. Refresh — 최신 Claude 기능 훑기 (Optional)

**이 Phase 는 선택이다.** 토큰·temperature·멀티턴·SDK 기본은 이미 안다고 가정한다.
여기선 2024~2026 사이에 **새로 쓰이게 된 기능들** 만 모아둔다.
건너뛰어도 되지만, Phase 1 Day 6 (prompt caching 전략) 부터는 Day 2 내용을 전제로 한다.

**언제 열 것인가**
- caching / thinking / batch / vision 중 한 번도 안 써봤다 → 훑고 가자 (5일)
- 다 편하다 → 스킵하고 Phase 1 로 직행

**기간**: 30분 × 5일 (전부 돌 경우)

## Day-by-Day

| Day | 주제 | 산출물 |
|---|---|---|
| 1 | Claude 4.x 모델 체계 (Opus 4.7 / Sonnet 4.6 / Haiku 4.5) — 언제 뭘 쓰나 | `models_decision.md` — 내 기준표 |
| 2 | Prompt Caching — `cache_control`, TTL, 계층화 | `caching_demo.py` (cache hit/miss 토큰 비교) |
| 3 | Extended Thinking (thinking blocks) — 언제 켜고 언제 끄나 | `thinking_demo.py` |
| 4 | Batch API / Files API — 대량 처리 & PDF 입력 | `batch_demo.py` |
| 5 | Vision / 멀티모달 — 이미지·PDF 페이지 넣기 | `multimodal_demo.py` |

## 참고

- Anthropic Docs: "Prompt caching", "Extended thinking", "Message Batches", "Files API", "Vision"
- Simon Willison weekly links — 새 기능 출시 때마다 샘플 제공
- YouTube: Anthropic 공식 채널 기능 소개 영상

## 본 과정으로

Phase 1 (`../01_context_eng/`) 로.
