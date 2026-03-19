agentA-html-views — Sprint 5

Previous Sprint Summary
─────────────────────────────────────────
- Sprint 4 shipped: bugfixes, /schema endpoint, install-skill
- Security hotfix: server now binds to 127.0.0.1
- Open: B-008 (HTML views), B-009 (config auth), F-013 (auto-collapse), F-014 (HTML views)
─────────────────────────────────────────

Sprint-Level Context

Goal
- Add HTML views for /status and /projects endpoints when accessed from a browser
- Add setup guide auto-collapse when Telegram is already connected
- Improve security of /api/config endpoint

Constraints
- Python 3.11+, use `python3` in all commands
- HTML views should be served when Accept header includes text/html, JSON otherwise
- Keep the dark theme consistent with config UI
- Agents run non-interactively — MUST NOT ask for confirmation or approval


Objective
- Add human-readable HTML views for /status and /projects endpoints

Tasks
- Modify `whatsup/server.py` — update `_handle_status()`:
  - Check if `Accept` header contains `text/html`
  - If HTML: render a styled page showing each transport's health with green/red indicators
  - If JSON (default): return JSON as before
  - Use the same dark theme CSS as config_ui.html
- Modify `whatsup/server.py` — update `_handle_projects()`:
  - Check if `Accept` header contains `text/html`
  - If HTML: render a styled page with a table of projects showing slug, transport, group ID, and notify events as badges
  - If JSON (default): return JSON as before
  - Include a link back to /config for editing
- Add a helper method `_wants_html(self) -> bool` that checks the Accept header
- Both HTML views should include the nav bar (Home, Config, Status, Projects, Schema) for navigation

Acceptance Criteria
- `curl http://localhost:1202/status` returns JSON (no Accept header = JSON default)
- Opening http://localhost:1202/status in a browser shows a styled HTML page with transport health
- Opening http://localhost:1202/projects in a browser shows a styled table of projects
- Both HTML views have navigation links and dark theme
