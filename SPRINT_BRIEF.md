# Sprint 5

Goal
- Add HTML views for /status and /projects endpoints when accessed from a browser
- Add setup guide auto-collapse when Telegram is already connected
- Improve security of /api/config endpoint

Constraints
- Python 3.11+, use `python3` in all commands
- HTML views should be served when Accept header includes text/html, JSON otherwise
- Keep the dark theme consistent with config UI
- Agents run non-interactively — MUST NOT ask for confirmation or approval

Merge Order
1. agentA-html-views
2. agentB-config-polish

Merge Verification
- python3 -c "from whatsup.server import WhatsupHandler; print('ok')"

Previous Sprint
- Sprint 4 shipped: bugfixes, /schema endpoint, install-skill
- Security hotfix: server now binds to 127.0.0.1
- Open: B-008 (HTML views), B-009 (config auth), F-013 (auto-collapse), F-014 (HTML views)

## agentA-html-views

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

## agentB-config-polish

Objective
- Auto-collapse setup guide when Telegram is connected, and add basic config endpoint protection

Tasks
- Modify `whatsup/config_ui.html`:
  - In the `load()` function, after fetching config, check if any project has `transport: "telegram"` with a non-empty `groupId`
  - If yes: auto-collapse the setup guide (set `guide-body` display to `none`)
  - If no: keep it expanded (user hasn't set up Telegram yet)
  - Add a small "Show setup guide" link that re-expands it
- Modify `whatsup/server.py` — add basic protection to `/api/config`:
  - Add `_handle_config_save`: check for a `X-Whatsup-Token` header or a `token` query parameter
  - The token is read from an env var `WHATSUP_API_TOKEN` — if set, all POST /api/config requests must include it
  - If `WHATSUP_API_TOKEN` is not set (default), no auth required (localhost-only is acceptable)
  - This prevents accidental writes from browser extensions or scripts without breaking the default experience
- Update README.md — add a "Security" section:
  - Server binds to 127.0.0.1 by default (not accessible from network)
  - Set `WHATSUP_API_TOKEN=mysecret` for config write protection
  - Set `WHATSUP_BIND=0.0.0.0` only if you need remote access (not recommended)

Acceptance Criteria
- Config UI auto-collapses setup guide when Telegram is configured
- "Show setup guide" link re-expands it
- When `WHATSUP_API_TOKEN` is set, POST /api/config without the token returns 403
- README has a Security section
