# Phase 5. MCP (Model Context Protocol)

**목표**: 한 번 짜면 Claude Desktop / Claude Code / 다른 호스트 모두에 붙는 표준 규격.
"LLM ↔ 내 데이터·툴·시스템" 을 연결하는 공용 컨센트.
MCP 서버를 **직접** 만들고, 내 워크플로에 꽂는다.

**기간**: 30분 × 10일

## Day-by-Day

| Day | 주제 | 산출물 |
|---|---|---|
| 1 | 읽기: modelcontextprotocol.io "Introduction" + "Concepts" | `mcp_overview.md` |
| 2 | MCP 3요소 이해: **Resources · Tools · Prompts** 구분 | `three_primitives.md` + 내 태스크 매핑 |
| 3 | 공식 python-sdk 로 "hello-world" 서버 | `servers/hello/` |
| 4 | Claude Desktop / Claude Code 에 연결 | `config_note.md` + 스크린샷 |
| 5 | Resources 서버: 내 로컬 문서를 LLM 에 노출 | `servers/docs/` |
| 6 | Tools 서버: 외부 API 래핑 (예: 날씨 · GitHub) | `servers/api_wrapper/` |
| 7 | Prompts 서버: 재사용 가능한 slash 커맨드 | `servers/prompts/` |
| 8 | **Code execution with MCP** (Anthropic 2025 블로그) | `code_exec_note.md` |
| 9 | 원격 MCP · OAuth · 팀 배포 고려사항 | `remote_mcp_note.md` |
| 10 | Mini-project: 내 개인 데이터용 MCP 서버 완성 | `servers/personal/` |

## 참고

- **modelcontextprotocol.io** (docs + spec)
- **Anthropic blog**: "Introducing MCP" (2024.11), "Code execution with MCP" (2025)
- **GitHub**: `anthropics/mcp-servers` — 공식 레퍼런스 서버들
- YouTube: Anthropic 공식 MCP 영상, AI Engineer MCP 세션
- Claude Code docs: MCP 설정 섹션

## 끝났을 때 할 줄 아는 것

- MCP 서버를 짠다 (Python SDK).
- Claude Code / Desktop 에 안정적으로 연결한다.
- "이건 tool 로 쓸지 resource 로 쓸지" 를 구분한다.
- 팀 배포 시 OAuth / 원격 MCP 옵션을 비교한다.

## 회고

- 배운 것 5개:
- 헷갈린 것 3개:
- 다음에 궁금한 것 3개:
