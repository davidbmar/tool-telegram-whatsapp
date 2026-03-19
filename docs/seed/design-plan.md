# Plan: tool-telegram-whatsapp — Multi-Transport Project Messaging for Afterburner

## Context

Afterburner needs a messaging layer for per-project group chats. Sprint events and manual checkins should post to the right group, scoped to that project. This is a **tiny standalone project** with four interfaces (REST, MCP, CLI, skill) and a **pluggable transport layer** — ship Telegram first (instant, zero friction), add WhatsApp when Business verification comes through.

**Name:** `tool-telegram-whatsapp`
**Repo:** New standalone project at `~/src/tool-telegram-whatsapp/`
**Transport (Phase 1):** Telegram Bot API — free, official, unlimited, instant setup
**Transport (Phase 2):** WhatsApp Business Cloud API — add when Meta Business verification is approved
**Size target:** ~400 lines of core code

---

## Architecture

```
tool-telegram-whatsapp/
├── whatsup/
│   ├── __init__.py              # Version, constants
│   ├── core.py                  # Core logic: send, notify, projects, status (~80 lines)
│   ├── config.py                # Load config from ~/.config/tool-telegram-whatsapp/ (~40 lines)
│   ├── messages.py              # Message formatters per event type (~50 lines)
│   ├── transport/
│   │   ├── __init__.py          # TransportProtocol base class (~20 lines)
│   │   ├── telegram.py          # Telegram Bot API client (~80 lines)
│   │   └── whatsapp.py          # WhatsApp Business Cloud API client (Phase 2, ~80 lines)
│   ├── server.py                # REST API on port 1202 (~60 lines)
│   └── mcp_server.py            # MCP server tools (~60 lines)
├── cli.py                       # CLI entry point (~50 lines)
├── pyproject.toml
└── README.md
```

### Four Interfaces, One Core

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
│   CLI    │  │   REST   │  │   MCP    │  │ Claude Skill │
│ whatsup  │  │ :1202    │  │ stdio    │  │ /whatsup     │
│ send ... │  │ /send    │  │ tools    │  │ (calls MCP)  │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘
     │             │             │                │
     └─────────────┴──────┬──────┴────────────────┘
                          │
                    whatsup/core.py
                          │
                    whatsup/transport/ (pluggable)
                     ┌─────┴─────┐
                 telegram.py  whatsapp.py
                     │            │
               Telegram API  WhatsApp Cloud API
                     │            │
               TG Groups    WA Groups
```

---

## Transport Protocol (pluggable)

```python
# whatsup/transport/__init__.py
from typing import Protocol

class Transport(Protocol):
    def send_message(self, group_id: str, text: str) -> dict: ...
    def create_group(self, name: str, members: list[str]) -> str: ...
    def health_check(self) -> dict: ...
```

Each transport implements this interface. Config selects which transport to use per project — so you could have some projects on Telegram and others on WhatsApp.

---

## Config Model

### `~/.config/tool-telegram-whatsapp/config.json`

```json
{
  "transports": {
    "telegram": {
      "botToken": "123456:ABC-DEF..."
    },
    "whatsapp": {
      "phoneNumberId": "123456789",
      "accessToken": "EAA..."
    }
  },
  "projects": {
    "grassyknoll": {
      "transport": "telegram",
      "groupId": "-1001234567890",
      "notify": ["sprint-merged", "test-failure", "checkin"]
    },
    "fsm-generic": {
      "transport": "telegram",
      "groupId": "-1009876543210",
      "notify": ["sprint-merged", "test-failure", "sprint-started", "checkin"]
    }
  }
}
```

---

## Interface Details

### 1. CLI (`cli.py`)

```bash
whatsup send grassyknoll "Deployed auth service to staging"
whatsup notify grassyknoll sprint-merged --sprint 7 --status passed --summary "Signal engine"
whatsup projects
whatsup status
whatsup create-group grassyknoll "GrassyKnoll Dev"
```

### 2. REST API (`server.py`) — port 1202

```
POST /send         — {slug, message}
POST /notify       — {slug, event, sprint, status, summary}
GET  /projects     — list configured projects + transport + group status
GET  /status       — per-transport health check
```

### 3. MCP Server (`mcp_server.py`)

```python
@mcp.tool()
async def send_checkin(slug: str, summary: str, details: str | None = None) -> str:
    """Send a checkin to a project's group chat."""

@mcp.tool()
async def send_notification(slug: str, event: str, sprint: int | None = None,
                            status: str | None = None, summary: str | None = None) -> str:
    """Send a sprint lifecycle notification."""

@mcp.tool()
async def whatsup_projects() -> str:
    """List projects with messaging configured."""

@mcp.tool()
async def whatsup_status() -> str:
    """Check transport connection status."""
```

### 4. Claude Skill (`/whatsup`)

`~/.claude/skills/whatsup.md`:
- `/whatsup <project> <message>` → send_checkin
- `/whatsup status` → whatsup_status
- `/whatsup projects` → whatsup_projects

---

## Afterburner Integration

### Sprint Hook (in consumer `.sprint/config.sh`)

```bash
WHATSAPP_ENABLED="${WHATSAPP_ENABLED:-false}"

if [ "$WHATSAPP_ENABLED" = "true" ]; then
  POST_MERGE_HOOKS+=("whatsup notify ${PROJECT_SLUG} sprint-merged --sprint \${SPRINT_NUM} --status \${TEST_STATUS} --summary \"\${SPRINT_GOAL}\"")
fi
```

---

## Message Formats

**Sprint merged:**
```
Sprint 7 merged — grassyknoll

3/3 branches · Tests PASSED · 45m

What shipped:
• Signal correlation engine
• 14 new tests
• Correlation UI panel
```

**Test failure:**
```
Sprint 7 FAILED — grassyknoll

Agent bravo merge failed verification
Exit code: 1
```

**Manual checkin:**
```
Checkin — grassyknoll
Deployed auth service to staging

OAuth2 flow working. Load test pending.
```

---

## Telegram Setup (5 minutes, Phase 1)

1. Message @BotFather on Telegram → `/newbot` → get bot token
2. Create Telegram groups for each project
3. Add the bot to each group
4. Get group chat IDs (send a message, check `getUpdates` API)
5. Add bot token + group IDs to `~/.config/tool-telegram-whatsapp/config.json`
6. Done — `whatsup send grassyknoll "hello"` works immediately

---

## Implementation Steps

### Phase 1: Core + Telegram + CLI + MCP

1. `mkdir ~/src/tool-telegram-whatsapp && cd ~/src/tool-telegram-whatsapp`
2. Create `pyproject.toml` with entry point `whatsup`
3. `whatsup/config.py` — load `~/.config/tool-telegram-whatsapp/config.json`
4. `whatsup/transport/__init__.py` — `Transport` protocol
5. `whatsup/transport/telegram.py` — Telegram Bot API (send_message via `requests`)
6. `whatsup/messages.py` — format_checkin, format_sprint_merged, format_test_failure
7. `whatsup/core.py` — send, notify, projects, status (delegates to transport)
8. `cli.py` — argparse: `whatsup send|notify|projects|status`
9. `whatsup/mcp_server.py` — MCP tools wrapping core.py
10. `~/.claude/skills/whatsup.md` — skill definition
11. Register in `.mcp.json`

### Phase 2: REST API + Afterburner hooks

- `whatsup/server.py` — standalone HTTP on port 1202
- Wire `POST_MERGE_HOOKS` in Afterburner sprint-config template
- Add `sprint-started`, `agent-completed` events
- History log: `~/.config/tool-telegram-whatsapp/history/<slug>.jsonl`

### Phase 3: WhatsApp transport

- `whatsup/transport/whatsapp.py` — WhatsApp Business Cloud API client
- Register message templates with Meta
- Projects can set `"transport": "whatsapp"` in config
- Mixed: some projects on Telegram, others on WhatsApp

---

## Verification

1. `pip install -e ~/src/tool-telegram-whatsapp`
2. Create Telegram bot + test group, configure config.json
3. `whatsup status` → shows Telegram transport healthy
4. `whatsup send test-project "Hello from tool-telegram-whatsapp"` → message in Telegram group
5. `whatsup notify test-project sprint-merged --sprint 1 --status passed --summary "Test"` → formatted message
6. MCP: `send_checkin("test-project", "Test checkin")` from Claude Code → message in group
7. `/whatsup test-project "Skill test"` from Claude Code → message in group
8. Sprint integration: run Afterburner sprint with `WHATSAPP_ENABLED=true` → notification after merge

---

## Dependencies

- Python 3.11+
- `requests` (HTTP calls to Telegram/WhatsApp APIs)
- `mcp` (MCP server)
- No other deps for Phase 1
