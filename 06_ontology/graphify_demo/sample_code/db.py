"""DB 연결 모듈 (sample_code 의 일부, 검색 대상)."""


class Database:
    """단순 in-memory DB 모킹."""

    def __init__(self):
        self._users = {}

    def get(self, key: str):
        return self._users.get(key)

    def put(self, key: str, value):
        self._users[key] = value


def connect(url: str) -> Database:
    """DB 인스턴스 생성. 실서비스라면 connection pool."""
    return Database()
