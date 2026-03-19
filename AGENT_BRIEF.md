agentB-schema-skill — Sprint 4

Previous Sprint Summary
─────────────────────────────────────────
- Sprint 3 shipped: console transport, whatsup init, 27 pytest tests, comprehensive README
- Open bugs: B-001 (MCP import), B-004 (__main__.py), B-005 (skill typo), B-006 (README URL)
- Open features: F-003 (install-skill), F-005 (schema endpoint), F-006 (register), F-008 (tool_config), F-010 (__main__)
─────────────────────────────────────────

Sprint-Level Context

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
