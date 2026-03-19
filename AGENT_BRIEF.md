agentA-gitignore-cleanup — Sprint 2

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
