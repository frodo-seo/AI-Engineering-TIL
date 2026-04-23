# Phase 3. RAG 심화

**목표**: "벡터DB 에 넣고 top-k" 수준을 넘어선다.
실전 RAG 가 쓰는 모든 개선을 **직접 돌리고 수치로 비교** 한다.

**기간**: 30분 × 15일

## Day-by-Day

| Day | 주제 | 산출물 |
|---|---|---|
| 1 | RAG 파이프라인 한 바퀴 (ingest → index → retrieve → answer) | `rag_v0.py` — 가장 순진한 버전 |
| 2 | Embedding 모델 비교: OpenAI vs Voyage vs Cohere vs bge | `embed_bench.md` |
| 3 | Chunking 전략: fixed / recursive / semantic / **late chunking** | `chunking_compare.py` |
| 4 | 벡터 DB 선택지: Chroma · Qdrant · pgvector 장단점 | `vectordb_note.md` |
| 5 | BM25 (키워드 검색) 다시 돌아보기 — 왜 여전히 중요한가 | `bm25_demo.py` |
| 6 | Hybrid search (BM25 + dense) + RRF 스코어 합성 | `hybrid_search.py` |
| 7 | Reranking: Cohere / Voyage / bge-reranker 비교 | `rerank_bench.md` |
| 8 | Query transformation: HyDE, decomposition, step-back | `query_transform.py` |
| 9 | **Anthropic Contextual Retrieval** 재현 (chunk 앞에 문맥 덧붙이기) | `contextual_rag.py` |
| 10 | Agentic RAG — 모델이 검색을 반복 호출 | `agentic_rag.py` |
| 11 | Citations / attribution (Anthropic Citations API) | `cite_demo.py` |
| 12 | RAG 평가 기초: faithfulness · answer relevance · context recall | `ragas_intro.md` |
| 13 | **Golden dataset 20개 직접 만들기** | `eval/golden.jsonl` |
| 14 | v0 → 최종 버전 정량 비교 | `rag_final.py` + `eval/report.md` |
| 15 | 회고 | README 하단 업데이트 |

## 참고

- **Anthropic blog**: "Contextual Retrieval"
- **Jason Liu**: "Levels of RAG" + RAG 강의 시리즈 (YouTube)
- **Eugene Yan**: "Patterns for building LLM-based systems"
- **LangChain YouTube**: *RAG from scratch* (Lance Martin) — 필수
- Chip Huyen *AI Engineering* 6장
- RAGAS / TruLens docs
- 논문: "Lost in the Middle" (Liu et al., 2023), "Late Chunking" (Jina)

## 끝났을 때 할 줄 아는 것

- Naive RAG vs Hybrid + Rerank + Contextual 의 성능 차이를 **수치로** 안다.
- Golden set 으로 RAG 를 회귀 테스트한다.
- "정답이 긴 문서 뒷부분", "동의어", "멀티홉" 각각에 어떤 기법이 유효한지 고른다.

## 회고

- 배운 것 5개:
- 헷갈린 것 3개:
- 다음에 궁금한 것 3개:
