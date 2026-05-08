# Phase 3. RAG 심화

**한 줄**: LLM 이 모르는 정보 (학습 이후, 비공개, 너무 많은 자료) 를 답변 직전에 검색해 prompt 에 끼워 넣는 패턴.

## 잡은 핵심 개념

### 임베딩 모델
- 텍스트 → 의미 공간의 벡터. 의미 가까우면 벡터 가깝게.
- **메커니즘**: encoder transformer (BERT 계열) + **contrastive 학습** (anchor / positive / negatives 로 같은 의미는 가깝게, 다른 의미는 멀게).
- LLM 과 같은 부품, 다른 학습. **단일 시퀀스 (next-token) vs 쌍 데이터 (contrastive)** 가 결정적 차이.
- **다국어**: 병렬 corpus 로 학습 → "dog" ↔ "강아지" 가 가까운 벡터. 영어 전용 모델이면 멀어짐.
- 평가: **MTEB / KO-MTEB leaderboard** 로 후보 추리고 → 본인 골든셋으로 Recall@k / MRR 직접 측정.
- AWS Bedrock 안: Cohere `embed-multilingual-v3` 가 한국어 1순위, Titan v2 는 차선.

### Chunking (RAG 품질의 1순위 변수)

우선순위 순:
1. **경계 존중** — 문장/단어/코드블록 중간에서 자르지 마라. recursive splitter 또는 구조 기반.
2. **크기 + overlap** — baseline 300~800 토큰 + overlap 10~20%. 본인 데이터로 측정해 결정.
3. **메타데이터 보존** — heading, source, section path 같이 저장.
4. **문서 타입별 전략** — 표·코드·PDF 는 함정 多.

### Hybrid Search

- **Vector** = 의미 일치, **BM25** = 정확 매칭. 둘 다 필요한 이유는 query 가 어느 쪽인지 미리 모르기 때문.
- **BM25** 는 inverted index 덕분에 query time 무료 + ms 단위. CPU only.
- **RRF (Reciprocal Rank Fusion)** = `Σ 1/(k+rank)`, k=60. 점수 정규화·가중치 튜닝 불필요. 실무 default.
- BM25 함정: 희소 토큰 매칭으로 의미 무관 청크가 top-k 진입 (예: "K2 소총" query → "K2 의류" 청크). hybrid + reranker 가 보완.

### Reranker (Cross-encoder)

- bi-encoder (임베딩) = query·청크 따로 인코딩 후 코사인.
- cross-encoder (rerank) = query+청크 **함께** 인코딩, 토큰 간 cross-attention. 정밀하지만 비싸서 1차 검색 후 top-100 에만.
- 한국어: **bge-reranker-v2-m3** (OSS, 무료) / **Cohere Rerank multilingual v3** (API, Bedrock).
- 표준 스택: `BM25+Vector → RRF top-100 → Reranker top-5 → LLM`.

### Prompt Caching

- **prefix 캐싱**. system + tools + few-shot 같은 정적 부분이 캐시.
- write 1.25x, read 0.1x. **재사용 횟수 N≥2 면 이득, N=1 이면 손해**. TTL 5분 (1h 옵션 있음).
- 함정: prefix 에 timestamp/ID 박으면 한 토큰 차이로 cache miss. **prefix 결정적이어야**.
- production 모니터링 필수: `cache_creation` vs `cache_read` 비율. hit rate < 30% 면 끄거나 재설계.

### Contextual Retrieval (Anthropic 2024.09)

- 청크 자체는 작게 자르되, 각 청크 앞에 "이 문서의 어떤 맥락인지" 50~100 토큰 prefix 를 LLM 이 자동 생성해 붙임.
- **검색 정확도 35% 개선 (논문)**.
- 비용은 prompt caching 으로 ~90% 절감. **인덱싱 1회성, 검색 매일** 이라 본전 빠르게 뽑힘.

### Batch API

- 24h SLA 양보 → input/output **50% 할인**.
- caching (×0.4 평균) + batch (×0.5) = 곱연산. OCR 같은 비실시간 + 정적 prefix 작업의 sweet spot.

## 참고

- Anthropic: "Contextual Retrieval" (2024.09)
- Jason Liu: "Levels of RAG"
- Eugene Yan: "Patterns for building LLM-based systems"
- LangChain YouTube: *RAG from scratch* (Lance Martin)
- Chip Huyen *AI Engineering* 6장
- 논문: "Lost in the Middle" (Liu et al., 2023), "Late Chunking" (Jina)
