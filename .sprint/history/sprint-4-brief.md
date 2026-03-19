# Sprint 4

Goal
- Fix all remaining bugs (MCP import, __main__.py, skill typo, README URL)
- Add /schema endpoint for tool plugin system integration
- Add `whatsup install-skill` command
- Polish for production readiness

Constraints
- Python 3.11+, use `python3` in all commands
- MCP import must be optional — tool should work without `mcp` package installed (graceful degradation)
- `__main__.py` should allow `python3 -m whatsup` to show help and `python3 -m whatsup.server` to start server
- Tests must still pass: `.venv/bin/python -m pytest tests/ -v`
- Agents run non-interactively — MUST NOT ask for confirmation or approval

Merge Order
1. agentA-bugfixes
2. agentB-schema-skill

Merge Verification
- python3 -c "from whatsup.core import send, notify, projects, status; print('core ok')"

Previous Sprint
- Sprint 3 shipped: console transport, whatsup init, 27 pytest tests, comprehensive README
- Open bugs: B-001 (MCP import), B-004 (__main__.py), B-005 (skill typo), B-006 (README URL)
- Open features: F-003 (install-skill), F-005 (schema endpoint), F-006 (register), F-008 (tool_config), F-010 (__main__)

## agentA-bugfixes

Objective
- Fix all open bugs and add __main__.py entry points

Tasks
- Fix B-001: Make MCP import optional in `whatsup/mcp_server.py`:
  - Wrap the `from mcp.server.fastmcp import FastMCP` import in a try/except
  - If `mcp` is not installed, define a stub that prints "MCP package not installed. Install with: pip install mcp" and exits
  - The rest of the package (CLI, REST, core) must work without `mcp` installed
- Fix B-004/F-010: Create `whatsup/__main__.py` (~15 lines):
  - When run as `python3 -m whatsup`, show help (delegate to cli.py main)
  - This also fixes `python3 -m whatsup.server` since Python resolves module paths
- Fix B-005: In `skills/whatsup.md`, change `python -m whatsup.mcp_server` to `python3 -m whatsup.mcp_server`
- Fix B-006: In `README.md`, change `yourorg` to `davidbmar` in the clone URL
- Fix B-002: In `whatsup/server.py`, rename `_Handler` to `WhatsupHandler` so it's importable
- Add `whatsup/__main__.py` that imports and calls `cli.main()`

Acceptance Criteria
- `python3 -c "from whatsup.core import send; print('ok')"` works (always worked, regression check)
- `python3 -m whatsup --help` shows CLI help
- `python3 -m whatsup.server --help` shows server help
- `python3 -c "from whatsup.server import WhatsupHandler; print('ok')"` works
- `grep 'davidbmar' README.md` finds the clone URL
- `grep 'python3' skills/whatsup.md` finds the corrected entry point
- MCP server gracefully prints error when `mcp` package is missing

## agentB-schema-skill

Objective
- Add GET /schema endpoint to REST server and `whatsup install-skill` CLI command

Tasks
- Add `GET /schema` endpoint to `whatsup/server.py`:
  - Returns JSON Schema describing the tool's per-project config:
    ```json
    {
      "tool": "tool-telegram-whatsapp",
      "version": "0.1.0",
      "description": "Per-project group-chat messaging via Telegram/WhatsApp",
      "globalConfig": {
        "type": "object",
        "properties": {
          "telegram": {
            "type": "object",
            "properties": {
              "botToken": {"type": "string", "description": "Telegram Bot API token", "sensitive": true}
            }
          },
          "console": {"type": "object", "properties": {}}
        }
      },
      "projectConfig": {
        "type": "object",
        "properties": {
          "transport": {"type": "string", "enum": ["telegram", "console", "whatsapp"], "default": "console"},
          "groupId": {"type": "string", "description": "Chat group ID"},
          "notify": {
            "type": "array",
            "items": {"type": "string", "enum": ["sprint-started", "agent-completed", "sprint-merged", "test-failure", "checkin"]},
            "default": ["sprint-merged", "test-failure"]
          }
        },
        "required": ["groupId"]
      }
    }
    ```
  - This is the schema that Afterburner's dashboard will read to render config forms (F-017 in Afterburner backlog)
- Add `install-skill` subcommand to `cli.py`:
  - `whatsup install-skill` — copies `skills/whatsup.md` to `~/.claude/skills/whatsup.md`
  - If file already exists, show diff and ask... no wait, non-interactive. Just overwrite and print "Skill installed to ~/.claude/skills/whatsup.md"
  - Create `~/.claude/skills/` directory if it doesn't exist
- Add test for `/schema` endpoint in `tests/test_cli.py` or new `tests/test_server.py`

Acceptance Criteria
- `curl http://localhost:1202/schema` returns valid JSON with `tool`, `globalConfig`, `projectConfig` fields
- `python3 cli.py install-skill` copies skill file to `~/.claude/skills/whatsup.md`
- Schema `projectConfig` has `transport`, `groupId`, `notify` properties
