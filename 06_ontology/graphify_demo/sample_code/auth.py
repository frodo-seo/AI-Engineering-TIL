"""인증 모듈 — 로그인 흐름. user/db 모듈에 의존."""

import hashlib

from db import connect
from user import find_user_by_email


def hash_password(password: str) -> str:
    """비밀번호를 sha256 해싱. 실서비스라면 bcrypt/argon2."""
    return hashlib.sha256(password.encode()).hexdigest()


def login(email: str, password: str) -> bool:
    """로그인 시도. 성공이면 True."""
    db = connect("local://")
    user = find_user_by_email(db, email)
    if user is None:
        return False
    return user.password_hash == hash_password(password)


def change_password(email: str, new_password: str) -> bool:
    """비밀번호 변경. find_user_by_email 로 사용자 존재 확인."""
    db = connect("local://")
    user = find_user_by_email(db, email)
    if user is None:
        return False
    user.password_hash = hash_password(new_password)
    return True
