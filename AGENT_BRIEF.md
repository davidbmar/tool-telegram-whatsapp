agentB-core-messages — Sprint 1

Sprint-Level Context

Goal
- Build the core Python package with pluggable transport layer and Telegram as the first transport
- Deliver CLI and MCP interfaces that can send messages to Telegram groups
- Install a Claude skill for conversational use

Constraints
- Python 3.11+, only dependencies are `requests` and `mcp`
- Config lives at `~/.config/tool-telegram-whatsapp/config.json` — never commit credentials
- All code goes in `whatsup/` package directory — do NOT create code outside this package (except cli.py and pyproject.toml at root)
- Use sync `requests` for HTTP calls (no async in core)
- Follow the Transport Protocol interface exactly: `send_message(group_id, text) -> dict`, `create_group(name, members) -> str`, `health_check() -> dict`
- Agents run non-interactively — MUST NOT ask for confirmation or approval. Proceed directly to implementation.
- Run `python -c "from whatsup import core; print('import ok')"` as a basic smoke test after implementation


Objective
- Create the core business logic and message formatting modules

Tasks
- Create `whatsup/messages.py` (~50 lines):
  - `format_checkin(slug: str, summary: str, details: str | None = None) -> str` — formats a manual checkin message
  - `format_sprint_merged(slug: str, sprint: int, branches: int = 0, status: str = "passed", summary: str = "") -> str` — formats a sprint merged notification
  - `format_test_failure(slug: str, sprint: int, agent: str = "", exit_code: int = 1) -> str` — formats a test failure notification
  - `format_event(event: str, **kwargs) -> str` — dispatcher that calls the right format function based on event name, raises ValueError for unknown events
  - Message formats should match these examples:
    - Checkin: `"Checkin — {slug}\n{summary}\n\n{details}"`
    - Sprint merged: `"Sprint {sprint} merged — {slug}\n\n{branches} branches · Tests {status}\n\n{summary}"`
    - Test failure: `"Sprint {sprint} FAILED — {slug}\n\nAgent {agent} merge failed verification\nExit code: {exit_code}"`
- Create `whatsup/core.py` (~80 lines):
  - `send(slug: str, message: str) -> dict` — load config, get project, instantiate transport, call send_message
  - `notify(slug: str, event: str, **data) -> dict` — check if event is in project's notify list, format message via messages.format_event, call send. Return `{"skipped": True, "reason": "..."}` if event not enabled.
  - `projects() -> list[dict]` — return all configured projects
  - `status() -> dict` — health check each unique transport, return dict of transport_name → health result
  - Import `config`, `messages`, and transport classes. Use a helper `_get_transport(transport_name: str, config: dict) -> Transport` that returns the right transport instance based on name ("telegram" → TelegramTransport).

Acceptance Criteria
- `from whatsup.messages import format_checkin, format_sprint_merged, format_test_failure, format_event` imports without error
- `format_checkin("test", "hello")` returns a string containing "Checkin" and "test"
- `format_event("sprint-merged", slug="test", sprint=1)` returns a string containing "Sprint 1 merged"
- `from whatsup.core import send, notify, projects, status` imports without error
