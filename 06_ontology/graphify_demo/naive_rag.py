"""Naive RAG — Phase 3 식 baseline.

흐름: 모든 파일을 청크로 자르고, query 와 BM25 점수가 높은 청크 top-k 반환.
구조 정보 (어디서 호출되나, 무엇에 의존하나) 를 알 수 없음. 텍스트 유사도만.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path

SAMPLE_DIR = Path(__file__).parent / "sample_code"


# ── 1. 청크 만들기 (10줄 단위) ───────────────────────────────────
def load_chunks() -> list[dict]:
    """sample_code 의 모든 .py 를 10줄짜리 청크로 분할."""
    chunks = []
    for path in SAMPLE_DIR.glob("*.py"):
        lines = path.read_text(encoding="utf-8").splitlines()
        for i in range(0, len(lines), 10):
            text = "\n".join(lines[i : i + 10])
            chunks.append(
                {"file": path.name, "start_line": i + 1, "text": text}
            )
    return chunks


# ── 2. BM25 (간소화 버전) ─────────────────────────────────────────
def tokenize(text: str) -> list[str]:
    """소문자화 + 영숫자 토큰만. 한국어 형태소 X."""
    return re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text.lower())


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.docs = docs
        self.N = len(docs)
        self.avg_len = sum(len(d) for d in docs) / max(self.N, 1)
        self.k1, self.b = k1, b
        self.df: Counter[str] = Counter()
        for d in docs:
            for term in set(d):
                self.df[term] += 1

    def idf(self, term: str) -> float:
        df = self.df.get(term, 0)
        return math.log((self.N - df + 0.5) / (df + 0.5) + 1)

    def score(self, query: list[str], doc_idx: int) -> float:
        doc = self.docs[doc_idx]
        tf = Counter(doc)
        dl = len(doc)
        s = 0.0
        for term in query:
            if term not in tf:
                continue
            num = tf[term] * (self.k1 + 1)
            denom = tf[term] + self.k1 * (1 - self.b + self.b * dl / self.avg_len)
            s += self.idf(term) * num / denom
        return s


# ── 3. 검색 ─────────────────────────────────────────────────────
def search(query: str, top_k: int = 3) -> list[dict]:
    chunks = load_chunks()
    docs = [tokenize(c["text"]) for c in chunks]
    bm25 = BM25(docs)
    q = tokenize(query)
    ranked = sorted(
        ((i, bm25.score(q, i)) for i in range(len(docs))),
        key=lambda x: x[1],
        reverse=True,
    )
    out = []
    for i, score in ranked[:top_k]:
        c = chunks[i]
        out.append({**c, "score": round(score, 3)})
    return out


if __name__ == "__main__":
    queries = [
        "find_user_by_email 함수가 어디서 호출돼?",
        "User 클래스는 어떤 모듈에 의존해?",
        "비밀번호 해싱은 어떻게 해?",
    ]
    for q in queries:
        print(f"\n>>> Q: {q}")
        for r in search(q):
            print(f"  [{r['file']}:L{r['start_line']}] score={r['score']}")
            preview = r["text"].splitlines()[0][:80]
            print(f"     {preview}")
