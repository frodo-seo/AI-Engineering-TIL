"""User 도메인 모듈 — DB 위에 사용자 조회·생성 기능."""

from db import Database, connect


class User:
    """사용자 도메인 객체."""

    def __init__(self, email: str, password_hash: str):
        self.email = email
        self.password_hash = password_hash


def find_user_by_email(db: Database, email: str) -> User | None:
    """이메일로 사용자 1명을 찾아 반환. 없으면 None."""
    raw = db.get(email)
    if raw is None:
        return None
    return User(email=raw["email"], password_hash=raw["password_hash"])


def create_user(db: Database, email: str, password_hash: str) -> User:
    """신규 사용자 등록."""
    db.put(email, {"email": email, "password_hash": password_hash})
    return User(email=email, password_hash=password_hash)
