# Afterburner Integration Points

## How tool-telegram-whatsapp Connects to Afterburner

### Sprint Lifecycle Events

The Afterburner sprint pipeline has natural notification points where tool-telegram-whatsapp hooks in:

| Event | Trigger Location | Data Available |
|-------|-----------------|----------------|
| Sprint started | `sprint-init.sh` completes | Goal, agents, phase count |
| Agent completed | `.agent-done-<name>` detected in polling loop | Agent name, duration, commit count |
| Sprint merged | POST_MERGE_HOOK fires in `sprint-run.sh` | SPRINT_NUM, ROOT, STATUS_FILE, SPRINT_BASE, TEST_STATUS |
| Test failure | Merge verification fails in `sprint-merge.sh` | Exit code, failing agent, sprint number |

### POST_MERGE_HOOKS (Primary Integration)

Afterburner's sprint scripts support an extensible hook system:
- Defined in `.sprint/config.sh` as `POST_MERGE_HOOKS` array
- Hooks run after report generation
- Receive env vars: `SPRINT_NUM`, `ROOT`, `STATUS_FILE`, `SPRINT_BASE`
- Hooks are non-fatal — failure logs a warning but doesn't block the pipeline

The CLI command `whatsup notify <slug> <event>` is designed to be called from these hooks.

### Existing Monitoring Infrastructure

Afterburner already has real-time monitoring that tool-telegram-whatsapp complements:
- **SSE streaming** — `/api/sprint-progress` streams agent status every 5 seconds
- **Polling** — `/api/sprint-live` returns sprint status (10-second refresh)
- **Dashboard views** — `sprint-live.js` and `sprint-progress.js` show per-agent cards

tool-telegram-whatsapp adds an **asynchronous notification channel** — you don't have to watch the dashboard. Key events come to your phone.

### Per-Project Configuration

Each Afterburner consumer project has `.sprint/config.sh` with project-specific settings. tool-telegram-whatsapp adds:

```bash
WHATSAPP_ENABLED="${WHATSAPP_ENABLED:-false}"
```

The project-to-group mapping lives in tool-telegram-whatsapp's own config (`~/.config/tool-telegram-whatsapp/config.json`), not in Afterburner. This keeps the coupling loose.

### Dashboard Integration (Future)

The Afterburner dashboard could show a messaging panel per project by calling tool-telegram-whatsapp's REST API:
- `GET /projects` — show which projects have messaging configured
- `GET /status` — show transport health
- Recent message history from `~/.config/tool-telegram-whatsapp/history/<slug>.jsonl`
