# Phase 6. GraphRAG

**한 줄**: vector RAG 가 약한 **구조적 / 시계열 / 멀티홉** 질문을 그래프 + LLM 으로 푸는 패러다임. 도메인 의존, optional.

## 잡은 핵심 개념

### Graphify vs Graphiti — 자주 혼동

| | **Graphify** | **Graphiti** (Zep) |
|---|---|---|
| 타겟 | 코드베이스 + 문서 RAG | 에이전트 메모리 (대화·이벤트) |
| 추출 | **AST (LLM 무료)** + 문서는 sub-agent | LLM 으로 entity·relation·timestamp |
| 그래프 | NetworkX + Leiden 클러스터링 | Neo4j |
| 시간 | 약함 | bi-temporal (valid + transaction time) |
| 강점 | "**71.5× 토큰 절감**" 클레임 | "에이전트가 시간 따라 학습" |

→ 이름 비슷해도 풀려는 문제 다름. 코딩/구조 → Graphify, 누적 메모리 → Graphiti.

### Graph RAG 의 토큰 절감 메커니즘

핵심: **LLM 한테 raw 청크 보내지 말고, 미리 추출한 정제 사실을 보내라.**

```
Naive RAG  → top-5 청크 ≈ 2,500 토큰을 LLM input 에
Graph RAG  → "callers: [auth.login, ...]" ≈ 30 토큰
```

분해:
1. **그래프 자체가 raw 의 압축** (10:1)
2. **결정적 응답** — false positive 0, top-k noise 없음 (3:1)
3. **raw text 안 보냄** — 정제 사실만 (3:1)
4. **인덱싱 무료** (Graphify 는 AST, LLM 안 부름)

→ 100 query 누적 시 ~80× 절감. 단 **구조 query 한정** (의미 query 면 vector RAG 가 여전히 default).

### 적용 가능 영역

| 도메인 | 적합도 |
|---|---|
| 코드베이스 (함수 관계, 영향범위, 호출 추적) | ★★★ Graphify |
| 에이전트 메모리 (사람·이벤트·관계 누적) | ★★★ Graphiti |
| 단순 PDF Q&A / FAQ | ✗ vector RAG 가 더 단순·저렴 |

### 산업 흐름 — 3패러다임 공존

> RAG 의 미래는 단일 패러다임이 아님.
> - **의미** → vector + hybrid (Phase 3)
> - **구조** → graph (Graphify)
> - **시간/관계** → temporal graph (Graphiti)

본인 데이터의 본질이 어느 쪽이냐에 맞춰 고름.

## 폴더 내용

- `graphify_demo/` — naive RAG vs graph RAG 의 토큰 절감 비교 데모
  - `sample_code/` — 미니 codebase (db / user / auth)
  - `naive_rag.py` — 10줄 청크 + BM25 top-k
  - `graph_rag.py` — AST → 그래프 (노드/엣지) → 구조 traversal
  - `compare.py` — 같은 query 두 RAG 에 던져 결과 나란히

```powershell
cd 06_ontology\graphify_demo
python compare.py
```

## 참고

- Microsoft Research: "From local to global: A GraphRAG approach" (2024)
- Zep: Graphiti GitHub (`getzep/graphiti`)
- LightRAG (HKU, 2024)
- Neo4j blog: LLM + Graph 시리즈
- 논문: GraphRAG, HippoRAG, LightRAG
