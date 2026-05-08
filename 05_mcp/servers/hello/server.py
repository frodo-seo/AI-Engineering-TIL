"""hello MCP server — 가장 단순한 MCP 서버.

이 파일이 곧 "서버" 다. 실행하면 stdio 로 MCP 프로토콜을 말하는 프로세스가 뜸.
host (Claude Desktop, Cursor, 너의 client 코드) 가 이걸 자식으로 띄우고
JSON-RPC 메시지로 통신함.

여기서 노출하는 primitive:
  - tool: get_weather(city)   — 한국 도시 mock 날씨
  - tool: echo(message)       — 입력 그대로 반환
"""

from mcp.server.fastmcp import FastMCP

# 서버 인스턴스. name 은 host 쪽 로그/UI 에 표시됨.
mcp = FastMCP("hello-mcp")


# ── tool 1 ─────────────────────────────────────────────────
# 함수 docstring → tool description
# 함수 시그니처 (타입힌트 포함) → input_schema 자동 생성
# 즉 Phase 2 에서 직접 짜던 schema 가 사라지고, Python 함수 그대로가 곧 tool.
@mcp.tool()
def get_weather(city: str) -> str:
    """한국 도시의 현재 날씨를 조회한다.

    Args:
        city: 한국 도시명 (한글). 예: "서울", "부산", "제주"
    """
    mock_weather = {
        "서울": "맑음, 22°C, 풍속 약함",
        "부산": "흐림, 19°C, 해풍 강함",
        "제주": "비, 18°C, 천둥",
        "대구": "맑음, 24°C",
    }
    return mock_weather.get(city, f"{city} 의 날씨 정보 없음.")


# ── tool 2 ─────────────────────────────────────────────────
@mcp.tool()
def echo(message: str) -> str:
    """입력 메시지를 그대로 돌려준다. 연결 테스트용."""
    return f"echo: {message}"


# ── 실행 ───────────────────────────────────────────────────
# stdio = 표준입출력으로 통신. host 가 이 스크립트를 subprocess 로 띄우면
# 자동으로 stdin/stdout 가 MCP 채널이 됨.
if __name__ == "__main__":
    mcp.run(transport="stdio")
