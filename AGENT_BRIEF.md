agentA-transport-config — Sprint 1

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
