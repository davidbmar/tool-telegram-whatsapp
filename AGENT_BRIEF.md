agentC-rest-server — Sprint 2

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
