# PROJECT STATUS — tool-telegram-whatsapp (Sprint 2)

**Date:** 2026-03-19
**Sprint:** 2
**Project:** tool-telegram-whatsapp

## Sprint 2 Summary

Added REST API server on port 1202, two new event types (sprint-started, agent-completed), real business logic in core.py (send/notify/projects/status), JSONL message history logging per project, and .gitignore cleanup. All 3 agents completed and merged cleanly.

---

## Merge Table

| # | Branch | Deliverable | Phase | Conflicts |
|---|--------|-------------|-------|-----------|
| 1 | agentA-gitignore-cleanup | .gitignore + removed committed __pycache__ from git | 1 | Clean |
| 2 | agentB-events-history | New event formatters (sprint-started, agent-completed), core.py business logic, JSONL history | 1 | Clean |
| 3 | agentC-rest-server | REST API server on :1202 with /send, /notify, /projects, /status, /history endpoints + CLI server subcommand | 1 | Clean |

## What Changed

### Cleanup
- `.gitignore` — standard Python ignores (pycache, eggs, venv, IDE files)
- Removed `__pycache__/` directories from git tracking

### New Event Types
- `whatsup/messages.py` — added `format_sprint_started()` and `format_agent_completed()` formatters, registered in `_FORMATTERS` dict

### Core Business Logic
- `whatsup/core.py` — rewritten with real `send()`, `notify()`, `projects()`, `status()` functions (was previously just re-exports)
- Event filtering: `notify()` checks project's `notify` list before sending

### History Logging
- `whatsup/history.py` — `log_message()` appends JSON lines to `~/.config/tool-telegram-whatsapp/history/<slug>.jsonl`, `get_history()` reads last N entries

### REST API Server
- `whatsup/server.py` — ThreadingHTTPServer on port 1202 with stale process cleanup, graceful shutdown
- Endpoints: POST /send, POST /notify, GET /projects, GET /status, GET /history
- `cli.py` — added `server` subcommand (`whatsup server --port 1202`)

## Capabilities

- All 4 planned interfaces now functional: CLI, REST, MCP, Skill
- 5 event types: checkin, sprint-merged, test-failure, sprint-started, agent-completed
- Per-project JSONL message history with read-back
- Stale process cleanup and graceful shutdown on REST server

## Next Steps

1. Sprint 3: WhatsApp Business Cloud API transport
2. Set up Telegram bot via @BotFather for live testing
3. Wire POST_MERGE_HOOKS in Afterburner sprint-config template
4. Tool plugin system design (registry, schema-driven config UI)

## Sessions

- S-2026-03-19-0406-gitignore-cleanup
- S-2026-03-19-0406-sprint2-events-history
- S-2026-03-19-0406-sprint2-rest-server
