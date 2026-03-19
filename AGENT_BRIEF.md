agentB-tests — Sprint 3

Previous Sprint Summary
─────────────────────────────────────────
- Sprint 2 shipped: REST API server on :1202, sprint-started + agent-completed formatters, real core.py business logic, JSONL history, .gitignore
- Known issues: MCP server can't import (`mcp` package not in system Python), no test suite, no sample config, README is scaffolding only
─────────────────────────────────────────

Sprint-Level Context

Goal
- Add comprehensive test suite so the tool is independently testable
- Fix MCP server dependency and make all interfaces work out of the box
- Add `whatsup init` command to generate sample config
- Add console transport for testing without Telegram credentials
- Write proper README.md with installation, quickstart, and API docs

Constraints
- Python 3.11+, use `python3` in all commands
- Tests use pytest — add `pytest` to dev dependencies in pyproject.toml
- Console transport prints to stdout instead of calling Telegram API — useful for testing and demos
- `whatsup init` creates `~/.config/tool-telegram-whatsapp/config.json` with a sample config using console transport
- README must be GitHub-ready with badges, installation, quickstart, config reference, and interface docs
- Agents run non-interactively — MUST NOT ask for confirmation or approval
- Existing imports must not break


Objective
- Create a comprehensive pytest test suite covering core, messages, config, history, and CLI

Tasks
- Create `tests/` directory with `__init__.py`
- Create `tests/conftest.py` (~30 lines):
  - Fixture `tmp_config` — creates a temporary config.json with console transport + demo project, sets env var or monkeypatches config path
  - Fixture `clean_history` — creates a temporary history directory
- Create `tests/test_messages.py` (~50 lines):
  - Test each of the 5 formatters returns correct strings
  - Test `format_event` dispatches correctly
  - Test `format_event` raises ValueError for unknown events
- Create `tests/test_config.py` (~40 lines):
  - Test `load_config` reads JSON file
  - Test `load_config` raises FileNotFoundError with helpful message when missing
  - Test `get_project` returns correct project
  - Test `get_project` raises ValueError for unknown slug
  - Test `get_all_projects` returns list
- Create `tests/test_core.py` (~50 lines):
  - Test `send()` with console transport — should succeed and return result
  - Test `notify()` with event in notify list — should send
  - Test `notify()` with event NOT in notify list — should return skipped
  - Test `projects()` returns list of projects
  - Test `status()` returns health check dict
- Create `tests/test_history.py` (~30 lines):
  - Test `log_message` creates JSONL file and appends
  - Test `get_history` reads back logged messages
  - Test `get_history` with limit
- Create `tests/test_cli.py` (~40 lines):
  - Test `whatsup --help` exits 0
  - Test `whatsup send demo "hello"` works with console transport
  - Test `whatsup projects` shows demo project
  - Test `whatsup status` shows console healthy
  - Use `subprocess.run` to test CLI as external process
- Note: all tests should use the console transport and temporary config — no Telegram credentials needed

Acceptance Criteria
- `python3 -m pytest tests/ -v` runs and all tests pass
- At least 15 tests covering messages, config, core, history, and CLI
- No tests require network access or real Telegram credentials
