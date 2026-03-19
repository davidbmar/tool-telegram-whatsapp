# Sprint 2

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

Merge Order
1. agentA-gitignore-cleanup
2. agentB-events-history
3. agentC-rest-server

Merge Verification
- python3 -c "from whatsup import core; from whatsup.messages import format_event, format_sprint_started, format_agent_completed; print('imports ok')"

Previous Sprint
- Sprint 1 shipped: config.py, transport/telegram.py, core.py (re-exports only), messages.py (checkin, sprint-merged, test-failure formatters), cli.py, mcp_server.py, skills/whatsup.md
- core.py currently has re-exports only — no send/notify/projects/status functions yet (MCP server inlines the logic)
- messages.py has _FORMATTERS dict for event dispatch

## agentA-gitignore-cleanup

Objective
- Add .gitignore and remove committed __pycache__ files

Tasks
- Create `.gitignore` at repo root with standard Python ignores:
  - `__pycache__/`, `*.pyc`, `*.pyo`, `*.egg-info/`, `dist/`, `build/`, `.eggs/`
  - `*.egg`, `.venv/`, `env/`, `.env`
  - `.pytest_cache/`, `.mypy_cache/`
  - IDE files: `.vscode/`, `.idea/`, `*.swp`, `*.swo`
- Remove all `__pycache__` directories from git tracking:
  - `git rm -r --cached whatsup/__pycache__/ whatsup/transport/__pycache__/`
  - Commit the removal

Acceptance Criteria
- `.gitignore` exists at repo root
- `git ls-files | grep __pycache__` returns nothing
- `python3 -c "from whatsup import core; print('ok')"` still works

## agentB-events-history

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

## agentC-rest-server

Objective
- Create the REST API server on port 1202

Tasks
- Create `whatsup/server.py` (~100 lines):
  - Use `http.server.HTTPServer` with `ThreadingMixIn` (match Afterburner's dashboard pattern)
  - Port 1202 (configurable via `--port` arg or `WHATSUP_PORT` env var)
  - Stale process cleanup on startup: kill any existing process on the port before binding
  - Graceful shutdown on SIGINT/SIGTERM
  - Startup logging: print port and loaded config
  - Endpoints:
    - `POST /send` — body `{"slug": "...", "message": "..."}`, calls `core.send()`, returns JSON result
    - `POST /notify` — body `{"slug": "...", "event": "...", "sprint": N, "status": "...", "summary": "...", "agent": "...", "exit_code": N}`, calls `core.notify()`, returns JSON result
    - `GET /projects` — calls `core.projects()`, returns JSON list
    - `GET /status` — calls `core.status()`, returns JSON dict
    - `GET /history?slug=...&limit=20` — calls `history.get_history()`, returns JSON list
  - Return `{"ok": true, "data": ...}` on success, `{"ok": false, "error": "..."}` on failure
  - Handle missing/invalid JSON body with 400 response
  - Handle unknown routes with 404
  - `main()` function with argparse for `--port`
- Update `cli.py` to add a `server` subcommand:
  - `whatsup server` — starts the REST server (calls `whatsup.server.main()`)
  - `whatsup server --port 1234` — custom port

Acceptance Criteria
- `python3 -m whatsup.server --help` or `python3 whatsup/server.py --help` shows port option
- `python3 -c "from whatsup.server import main; print('import ok')"` works
- Server starts on port 1202, logs startup message, and responds to `GET /status` with JSON
- `whatsup server` subcommand appears in `python3 cli.py --help`
