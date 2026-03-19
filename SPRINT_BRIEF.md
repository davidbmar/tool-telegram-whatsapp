# Sprint 1

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

Merge Order
1. agentA-transport-config
2. agentB-core-messages
3. agentC-cli-mcp-skill

Merge Verification
- python -c "from whatsup import core; print('import ok')"

## agentA-transport-config

Objective
- Create the project packaging, config loader, and pluggable transport layer with Telegram implementation

Tasks
- Create `pyproject.toml` with package name `whatsup`, Python >=3.11, dependencies `requests` and `mcp`, and entry point `whatsup = "cli:main"`
- Create `whatsup/__init__.py` with `__version__ = "0.1.0"`
- Create `whatsup/config.py` (~40 lines):
  - `load_config() -> dict` — reads `~/.config/tool-telegram-whatsapp/config.json`, returns parsed JSON
  - `get_project(slug: str) -> dict` — returns project config (transport, groupId, notify list) or raises ValueError
  - `get_all_projects() -> list[dict]` — returns all configured projects with their slugs
  - If config file doesn't exist, raise FileNotFoundError with helpful message pointing to the expected path
- Create `whatsup/transport/__init__.py` (~20 lines):
  - Define `Transport` as a `typing.Protocol` with three methods: `send_message(self, group_id: str, text: str) -> dict`, `create_group(self, name: str, members: list[str]) -> str`, `health_check(self) -> dict`
  - Export `Transport`
- Create `whatsup/transport/telegram.py` (~80 lines):
  - Class `TelegramTransport` implementing the Transport protocol
  - Constructor takes `bot_token: str`
  - `send_message` — POST to `https://api.telegram.org/bot{token}/sendMessage` with `chat_id` and `text` params, return response JSON
  - `create_group` — POST to `createChatInviteLink` (Telegram can't create groups via bot API, so just create an invite link for an existing group), return the invite link
  - `health_check` — GET `https://api.telegram.org/bot{token}/getMe`, return bot info dict on success, `{"ok": False, "error": str}` on failure
  - Handle request errors gracefully — return error dicts, don't raise

Acceptance Criteria
- `from whatsup.config import load_config, get_project` imports without error
- `from whatsup.transport import Transport` imports without error
- `from whatsup.transport.telegram import TelegramTransport` imports without error
- TelegramTransport implements all 3 Transport protocol methods
- Config loader returns meaningful errors when file is missing

## agentB-core-messages

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

## agentC-cli-mcp-skill

Objective
- Create the CLI entry point, MCP server, and Claude skill file

Tasks
- Create `cli.py` (~50 lines) at repo root:
  - Uses `argparse` with subcommands: `send`, `notify`, `projects`, `status`
  - `send <slug> <message>` — calls `core.send(slug, messages.format_checkin(slug, message))`
  - `notify <slug> <event>` with optional `--sprint`, `--status`, `--summary`, `--agent`, `--exit-code` flags — calls `core.notify(slug, event, **kwargs)`
  - `projects` — calls `core.projects()`, prints as formatted table
  - `status` — calls `core.status()`, prints transport health
  - `main()` function as entry point, handles errors with sys.exit(1) and user-friendly messages
- Create `whatsup/mcp_server.py` (~60 lines):
  - Import `mcp` package and create server: `mcp = Server("tool-telegram-whatsapp")`
  - Tool `send_checkin(slug: str, summary: str, details: str | None = None) -> str` — wraps core.send with messages.format_checkin
  - Tool `send_notification(slug: str, event: str, sprint: int | None = None, status: str | None = None, summary: str | None = None) -> str` — wraps core.notify
  - Tool `whatsup_projects() -> str` — wraps core.projects, returns JSON string
  - Tool `whatsup_status() -> str` — wraps core.status, returns JSON string
  - `if __name__ == "__main__"` or `def main()` that runs the MCP server via stdio
- Create `skills/whatsup.md` in the repo (to be installed to `~/.claude/skills/`):
  - Skill name: whatsup
  - When user says `/whatsup <project> <message>` → call `send_checkin` MCP tool
  - When user says `/whatsup status` → call `whatsup_status` MCP tool
  - When user says `/whatsup projects` → call `whatsup_projects` MCP tool
  - Include clear trigger description and usage examples

Acceptance Criteria
- `python cli.py --help` prints usage with send, notify, projects, status subcommands
- `python cli.py send --help` shows slug and message as required args
- `from whatsup.mcp_server import mcp` imports without error (or equivalent server object)
- `skills/whatsup.md` exists and contains skill definition with trigger, usage, and MCP tool mappings
