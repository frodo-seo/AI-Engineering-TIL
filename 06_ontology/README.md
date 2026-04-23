# Phase 6. Ontology & GraphRAG

**목표**: 벡터 검색만으로 안 풀리는 **관계형 질문** —
"A·B 의 공통 상사는?", "이 프로젝트에 영향 준 사람들은?", "이 결정은 누가 언제 뒤집었나?" —
을 **지식그래프 + LLM** 으로 푸는 법.

**기간**: 30분 × 10일

## Day-by-Day

| Day | 주제 | 산출물 |
|---|---|---|
| 1 | 왜 그래프인가: 벡터 RAG 가 실패하는 질문 사례 수집 | `why_graph.md` |
| 2 | 지식그래프 기초: entity · relation · property | `kg_basics.md` |
| 3 | LLM 으로 entity extraction (schema 기반) | `extract_entities.py` |
| 4 | Entity resolution — 같은 인물·개념 병합 | `entity_resolution.py` |
| 5 | **Microsoft GraphRAG** 논문 & 블로그 정독 | `graphrag_summary.md` |
| 6 | Neo4j (또는 Kuzu) 로 작은 KG 만들기 | `build_kg.py` |
| 7 | Cypher 쿼리 감 잡기 | `cypher_drills.md` |
| 8 | Community detection → 요약 (GraphRAG 의 핵심 아이디어) | `community_summary.py` |
| 9 | Hybrid: vector + graph (LightRAG 스타일) | `hybrid_kg.py` |
| 10 | Mini-project: 내 Obsidian · 노트 → 지식그래프 | `mini_kg/` |

## 참고

- **Microsoft Research**: "From local to global: A GraphRAG approach" (2024)
- **LightRAG** (HKU, 2024)
- **Neo4j blog**: LLM + Graph 시리즈
- YouTube: Neo4j 공식 GraphRAG 영상, Matthew Berman GraphRAG 해설
- Palantir 관점: "Ontology" 는 체계적 데이터 모델링의 이름 — 제품팀이 공유하는 어휘
- 논문: GraphRAG, HippoRAG, LightRAG

## 끝났을 때 할 줄 아는 것

- "이 질문은 벡터로 안 풀린다" 는 순간을 구별한다.
- LLM 으로 문서 → KG 파이프라인을 짠다.
- GraphRAG 가 naive RAG 보다 유리한 질문 유형을 설명한다.

## 회고

- 배운 것 5개:
- 헷갈린 것 3개:
- 다음에 궁금한 것 3개:
