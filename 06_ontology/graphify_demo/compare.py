"""같은 query 를 두 RAG 에 던져 retrieved context 를 나란히 비교.

목적: "구조적 query 에서 graph RAG 가 왜 압도적인가" 를 눈으로 보기.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from graph_rag import build_graph, search as graph_search
from naive_rag import search as naive_search

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


QUERIES = [
    "find_user_by_email 함수가 어디서 호출돼?",
    "User 클래스는 어떤 모듈에 의존해?",
    "비밀번호 해싱은 어떻게 해?",
]


def run():
    g = build_graph()

    for q in QUERIES:
        print("\n" + "█" * 76)
        print(f" Q: {q}")
        print("█" * 76)

        # ── Naive RAG ──
        print("\n[Naive RAG — BM25 top-3]")
        for r in naive_search(q, top_k=3):
            print(f"  📄 {r['file']}:L{r['start_line']}  (score={r['score']})")
            for line in r["text"].splitlines()[:3]:
                print(f"     {line}")
        print(
            "  → 텍스트 일치 청크 반환. '어디서 호출되는지' 같은 구조 정보 없음."
        )

        # ── Graph RAG ──
        print("\n[Graph RAG — AST + 그래프 탐색]")
        r = graph_search(q, g)
        if r["matched_nodes"]:
            print(f"  🔵 matched nodes: {[m['id'] for m in r['matched_nodes']]}")
        else:
            print("  🔵 매칭된 노드 없음 (식별자 기반 query 가 아닌 듯)")
        for nid, callers in r["callers"].items():
            print(f"  ➡  '{nid}' 호출자: {callers}")
        for nid, deps in r["deps"].items():
            print(f"  ➡  '{nid}' 의존: {deps}")
        if not r["callers"] and not r["deps"]:
            print(
                "  → 구조적 답이 없음 (이 query 는 의미 검색이 더 나을 수 있음)"
            )


if __name__ == "__main__":
    run()
