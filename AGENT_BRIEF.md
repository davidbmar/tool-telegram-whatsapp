agentB-events-history — Sprint 2

Previous Sprint Summary
─────────────────────────────────────────
- Sprint 1 shipped: config.py, transport/telegram.py, core.py (re-exports only), messages.py (checkin, sprint-merged, test-failure formatters), cli.py, mcp_server.py, skills/whatsup.md
- core.py currently has re-exports only — no send/notify/projects/status functions yet (MCP server inlines the logic)
- messages.py has _FORMATTERS dict for event dispatch
─────────────────────────────────────────

Sprint-Level Context

Goal
- Add REST API server on port 1202 for HTTP-based integrations
- Add new event types: sprint-started, agent-completed
- Add JSONL message history logging per project
- Add .gitignore and clean up __pycache__ from repo

Constraints
- Python 3.11+, only dependencies are `requests` and `mcp`
- Use stdlib `http.server` for the REST API (no FastAPI) to match Afterburner's pattern
- REST server runs standalone on port 1202 — must include stale process cleanup and graceful shutdown
- History logs go to `~/.config/tool-telegram-whatsapp/history/<slug>.jsonl`
- All verification commands must use `python3` not `python`
- Agents run non-interactively — MUST NOT ask for confirmation or approval
- Existing imports must not break: `from whatsup import core`, `from whatsup.messages import format_event`


Objective
- Add sprint-started and agent-completed event formatters, refactor core.py with real business logic, and add JSONL history logging

Tasks
- Add to `whatsup/messages.py`:
  - `format_sprint_started(slug: str, sprint: int, goal: str = "", agents: str = "", phases: int = 1) -> str` — format: `"Sprint {sprint} started — {slug}\n\nGoal: {goal}\nAgents: {agents}\nPhases: {phases}"`
  - `format_agent_completed(slug: str, sprint: int, agent: str, duration: str = "", commits: int = 0, remaining: int = 0) -> str` — format: `"Agent {agent} completed — {slug} Sprint {sprint}\n\n{duration} · {commits} commits\n{remaining} agents remaining"`
  - Register both in `_FORMATTERS` dict: `"sprint-started"` and `"agent-completed"`
- Rewrite `whatsup/core.py` (~80 lines) with actual business logic (NOT just re-exports):
  - `send(slug: str, message: str) -> dict` — load config, get project, instantiate transport, call send_message, log to history, return result
  - `notify(slug: str, event: str, **data) -> dict` — check if event is in project's notify list, format message via messages.format_event, call send. Return `{"skipped": True, "reason": "..."}` if event not enabled.
  - `projects() -> list[dict]` — return all configured projects with slugs
  - `status() -> dict` — health check each unique transport
  - Helper `_get_transport(transport_name: str, transports_config: dict)` — returns TelegramTransport instance based on name
  - Keep existing re-exports at top of file so `from whatsup import core` still works for backwards compat
- Create `whatsup/history.py` (~40 lines):
  - `log_message(slug: str, direction: str, event: str, message: str, result: dict) -> None` — append a JSON line to `~/.config/tool-telegram-whatsapp/history/{slug}.jsonl`
  - Each line: `{"timestamp": "ISO8601", "direction": "outbound", "event": "sprint-merged", "message": "...", "result": {...}}`
  - Create history directory if it doesn't exist
  - `get_history(slug: str, limit: int = 20) -> list[dict]` — read last N lines from the JSONL file, return as list of dicts

Acceptance Criteria
- `from whatsup.messages import format_sprint_started, format_agent_completed` imports without error
- `format_event("sprint-started", slug="test", sprint=1)` returns string containing "Sprint 1 started"
- `format_event("agent-completed", slug="test", sprint=1, agent="alpha")` returns string containing "Agent alpha completed"
- `from whatsup.core import send, notify, projects, status` imports real functions (not just re-exports)
- `from whatsup.history import log_message, get_history` imports without error
