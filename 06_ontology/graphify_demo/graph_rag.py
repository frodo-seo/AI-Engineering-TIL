"""Graphify-style RAG — AST 로 코드 구조를 그래프로 만들고 그래프를 탐색.

핵심 차이 (vs naive_rag.py):
  - 임베딩·BM25 안 씀. 표준 라이브러리 `ast` 의 결정적 파싱 사용.
  - 노드 = 함수/클래스/파일, 엣지 = 호출/import/상속.
  - query 의 식별자를 노드로 lookup → 그래프를 traverse 해서
    "이게 어디서 호출되나 / 무엇에 의존하나 / 뭐랑 같이 쓰이나" 같은
    구조적 답을 정확히 반환.
"""

from __future__ import annotations

import ast
from pathlib import Path

SAMPLE_DIR = Path(__file__).parent / "sample_code"


# ── 그래프 자료구조 (NetworkX 안 쓰고 dict 로 충분) ──────────────
class CodeGraph:
    def __init__(self):
        # node_id (str) → metadata
        self.nodes: dict[str, dict] = {}
        # 엣지 저장 — (from, to, kind) 튜플 리스트
        self.edges: list[tuple[str, str, str]] = []

    def add_node(self, node_id: str, **meta):
        self.nodes[node_id] = {**meta, "id": node_id}

    def add_edge(self, src: str, dst: str, kind: str):
        self.edges.append((src, dst, kind))

    def neighbors(self, node_id: str, kind: str | None = None, direction: str = "out"):
        """direction: 'out' = src 가 node 인 엣지, 'in' = dst 가 node 인 엣지."""
        for s, d, k in self.edges:
            if kind and k != kind:
                continue
            if direction == "out" and s == node_id:
                yield d, k
            elif direction == "in" and d == node_id:
                yield s, k


# ── AST 로 그래프 빌드 ─────────────────────────────────────────
def build_graph() -> CodeGraph:
    g = CodeGraph()

    for path in SAMPLE_DIR.glob("*.py"):
        module_name = path.stem
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        # 파일 자체를 모듈 노드로
        g.add_node(module_name, kind="module", file=path.name)

        for node in ast.walk(tree):
            # import 추적
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.ImportFrom) and node.module:
                    g.add_edge(module_name, node.module, "imports")
                    for alias in node.names:
                        # "from db import Database" → module 이 Database 사용
                        g.add_edge(module_name, alias.name, "uses_symbol")
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        g.add_edge(module_name, alias.name, "imports")

            # 함수 정의
            elif isinstance(node, ast.FunctionDef):
                fn_id = f"{module_name}.{node.name}"
                g.add_node(
                    fn_id, kind="function", module=module_name, line=node.lineno
                )
                g.add_edge(module_name, fn_id, "defines")

                # 함수 안의 호출 추적
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Call):
                        target = _call_target_name(sub)
                        if target:
                            g.add_edge(fn_id, target, "calls")

            # 클래스 정의
            elif isinstance(node, ast.ClassDef):
                cls_id = f"{module_name}.{node.name}"
                g.add_node(
                    cls_id, kind="class", module=module_name, line=node.lineno
                )
                g.add_edge(module_name, cls_id, "defines")

                # 클래스 안의 메서드도 함수로
                for body in node.body:
                    if isinstance(body, ast.FunctionDef):
                        m_id = f"{cls_id}.{body.name}"
                        g.add_node(
                            m_id, kind="method", parent=cls_id, line=body.lineno
                        )
                        g.add_edge(cls_id, m_id, "has_method")

    return g


def _call_target_name(call: ast.Call) -> str | None:
    """ast.Call 노드에서 호출 대상 이름 추출."""
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return None


# ── 검색 (구조적 query) ────────────────────────────────────────
def find_callers(g: CodeGraph, name: str) -> list[str]:
    """주어진 이름을 호출하는 함수들. (calls 엣지의 destination 검색)"""
    callers = []
    for s, d, k in g.edges:
        if k == "calls" and d == name:
            callers.append(s)
    return callers


def find_dependencies(g: CodeGraph, module: str) -> list[tuple[str, str]]:
    """이 모듈이 의존하는 것들 (imports / uses_symbol)."""
    deps = []
    for d, k in g.neighbors(module, direction="out"):
        if k in ("imports", "uses_symbol"):
            deps.append((d, k))
    return deps


def search(query: str, g: CodeGraph) -> dict:
    """간단한 자연어 → 구조 query 라우팅 (실제 graphify 는 더 정교).

    여기선 query 안 식별자 + 키워드로 의도 추정.
    """
    # query 안에 등장하는 식별자 후보 추출
    import re

    candidates = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", query)
    known = [c for c in candidates if any(c in nid for nid in g.nodes)]

    result = {"query": query, "matched_nodes": [], "callers": {}, "deps": {}}

    for name in known:
        # 노드 정확 매칭 또는 suffix 매칭
        matched = [nid for nid in g.nodes if nid.endswith("." + name) or nid == name]
        for nid in matched:
            result["matched_nodes"].append({"id": nid, **g.nodes[nid]})

            # 호출자 탐색
            callers = find_callers(g, name)
            if callers:
                result["callers"][nid] = callers

            # 의존성 탐색 (모듈 노드인 경우)
            if g.nodes[nid].get("kind") == "module":
                result["deps"][nid] = find_dependencies(g, nid)

    return result


if __name__ == "__main__":
    g = build_graph()

    print(f"=== 그래프 빌드 결과 ===")
    print(f"  노드: {len(g.nodes)}개")
    print(f"  엣지: {len(g.edges)}개")
    print()
    print("  노드 샘플:")
    for nid, meta in list(g.nodes.items())[:8]:
        print(f"    {nid}  ({meta.get('kind')})")
    print("  엣지 샘플:")
    for s, d, k in g.edges[:8]:
        print(f"    {s}  --[{k}]-->  {d}")

    print("\n\n=== 구조적 query ===")
    queries = [
        "find_user_by_email 함수가 어디서 호출돼?",
        "User 클래스는 어떤 모듈에 의존해?",
        "비밀번호 해싱은 어떻게 해?",
    ]
    for q in queries:
        print(f"\n>>> Q: {q}")
        r = search(q, g)
        print(f"  matched: {[m['id'] for m in r['matched_nodes']]}")
        for nid, callers in r["callers"].items():
            print(f"  '{nid}' 호출자: {callers}")
        for nid, deps in r["deps"].items():
            print(f"  '{nid}' 의존: {deps}")
