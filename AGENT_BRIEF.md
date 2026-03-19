agentC-cli-mcp-skill — Sprint 1

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
