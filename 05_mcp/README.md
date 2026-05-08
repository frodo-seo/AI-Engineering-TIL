# Phase 5. MCP (Model Context Protocol)

**한 줄**: LLM 앱과 외부 도구·데이터를 잇는 표준 프로토콜. "AI 의 USB-C", IDE 의 LSP 가 했던 일을 LLM 통합에.

## 잡은 핵심 개념

### 본질 — LLM 측 변화 0, 패키징 표준

> Phase 2 의 tool use 와 LLM 시점에서 100% 동일.
> 차이는 host 측에만 있음 — tool 정의가 host 코드 안 hardcoded vs 외부 server 에서 import.

가치 = **N×M 통합 폭발을 N+M 으로**. 한 번 짠 server 가 Claude Desktop / Cursor / 본인 agent 모두에서 사용 가능.

### 아키텍처 — 3 역할

- **Host** — LLM 앱 (Claude Desktop, Cursor, 본인 코드)
- **Client** — host 안에서 server 1개와 1:1 연결
- **Server** — 도구·데이터 노출 (Slack, Postgres, filesystem 등)

### 3 Primitive

- **Tools** — LLM 이 자율 호출하는 함수 (Phase 2 의 그것)
- **Resources** — read-only 데이터, 사용자가 첨부
- **Prompts** — 슬래시 커맨드 같은 prompt 템플릿

### Transport

- **stdio** — host 가 server 를 자식 프로세스로 띄움. 포트 X. 학습/개인 use 의 99%.
- **HTTP / Streamable HTTP** — 원격 server, enterprise 배포.

### 흐름 (LLM 은 MCP 모름)

```
1. host 시작 시 — 한 번:
   host → MCP server: list_tools → tool 정의 받음
2. user query:
   host → Claude API: messages + (MCP 에서 받은) tools
3. Claude → tool_use 블록 (Phase 2 와 동일)
4. host → MCP server: call_tool (라우팅)
5. server 실제 함수 실행 → host → Claude → 자연어 답변
```

→ Claude ↔ host = 일반 Anthropic API, host ↔ server = MCP 프로토콜. **두 채널 분리, LLM 은 MCP 단어조차 모름**.

### CLI vs MCP — 실용주의 균형

> "CLI 가 핫하다" = LLM 이 이미 git/bash/psql/kubectl 등을 학습 완료. 새 API 짜기 전에 bash 부터 줘봐라.

도구 선택 3단:
1. **bash + 기존 CLI** 로 됨? → 끝
2. **in-code 함수 (Phase 2 식)** 로 됨? → 끝 (한 host 에서만 쓰면)
3. 위 둘로 안 되거나 **여러 host 공유** 필요 → **MCP server**

핵심: "복잡함" 만으로 MCP 결정 X. **공유 범위** 가 진짜 결정 요인.

## 폴더 내용

- `servers/hello/server.py` — FastMCP 로 짠 minimal MCP server (`get_weather`, `echo` tool 노출)
- `servers/hello/client_demo.py` — LLM 없이 MCP 프로토콜만 검증하는 pure client

```powershell
# 검증
cd 05_mcp\servers\hello
python client_demo.py
# 또는
mcp dev server.py    # 웹 inspector
```

## 참고

- modelcontextprotocol.io (docs + spec)
- Anthropic: "Introducing MCP" (2024.11), "Code execution with MCP" (2025)
- GitHub: `anthropics/mcp-servers` (공식 레퍼런스 server 들)
