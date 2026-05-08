"""hello MCP client demo — server.py 가 잘 동작하는지 LLM 없이 검증.

흐름 (Phase 5 의 핵심 그림):
  1. server.py 를 자식 프로세스로 띄움 (stdio transport)
  2. ClientSession 으로 handshake (initialize)
  3. list_tools() — 서버가 노출한 tool 정의 목록 받음
  4. call_tool(name, args) — 그 tool 을 호출하고 결과 받음

이게 host 가 LLM 호출 직전·직후에 하는 일 그대로다.
LLM 만 빠진 셈. LLM 끼우면 4번을 LLM 의 tool_use 결정으로 바꾸면 됨.
"""

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main():
    # 서버 띄우는 명령어. host 가 자식 프로세스로 실행할 것.
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],  # 이 데모는 hello/ 안에서 실행한다고 가정
    )

    # stdio_client = (read, write) 스트림 페어 만듦
    async with stdio_client(server_params) as (read, write):
        # ClientSession = MCP 프로토콜 레이어 (JSON-RPC 처리)
        async with ClientSession(read, write) as session:
            # handshake — 양쪽 capability 교환
            await session.initialize()

            # 1. 서버가 어떤 tool 가지고 있나
            print(">>> list_tools()")
            tools = await session.list_tools()
            for t in tools.tools:
                print(f"  - {t.name}: {t.description.splitlines()[0]}")
                print(f"      schema: {t.inputSchema}")

            # 2. tool 호출 — get_weather
            print("\n>>> call_tool('get_weather', city='서울')")
            result = await session.call_tool("get_weather", {"city": "서울"})
            for c in result.content:
                if c.type == "text":
                    print(f"  result: {c.text}")

            # 3. 다른 tool 호출 — echo
            print("\n>>> call_tool('echo', message='hello mcp')")
            result = await session.call_tool("echo", {"message": "hello mcp"})
            for c in result.content:
                if c.type == "text":
                    print(f"  result: {c.text}")


if __name__ == "__main__":
    asyncio.run(main())
