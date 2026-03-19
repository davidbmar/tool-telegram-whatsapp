# Roadmap & Architecture

## Roadmap

### Current Focus
**Sprint 1: Core + Telegram + CLI + MCP.** Build the Python package with the pluggable transport layer, Telegram as the first transport, CLI and MCP server as the primary interfaces, and a Claude skill for conversational use. End-to-end goal: `whatsup send grassyknoll "hello"` delivers a message to a Telegram group.

### Next Up
1. **Sprint 2: REST API + Afterburner hooks** — Add HTTP server on port 1202, wire POST_MERGE_HOOKS in Afterburner's sprint-config template, add sprint-started and agent-completed events, JSONL history logging.
2. **Sprint 3: WhatsApp transport** — Implement WhatsApp Business Cloud API client, register message templates with Meta, enable per-project transport selection (some projects on Telegram, others on WhatsApp).
3. **Future: Dashboard integration** — Afterburner dashboard panel showing messaging status and recent messages per project via REST API.

## Architecture

### System Overview
```
~/.config/tool-telegram-whatsapp/config.json
        │
        ▼
┌─────────────────────────────────────────┐
│  whatsup package                        │
│                                         │
│  config.py ← reads project→group map    │
│       │                                 │
│  core.py  ← business logic              │
│   │    │                                │
│   │  messages.py ← format per event     │
│   │                                     │
│  transport/                             │
│   ├── __init__.py  ← Protocol class     │
│   ├── telegram.py  ← Bot API client     │
│   └── whatsapp.py  ← Cloud API client   │
└──┬──────┬──────┬──────┬────────────────┘
   │      │      │      │
 cli.py server mcp_srv skill
   │      │      │      │
 shell  HTTP   stdio  Claude
 hooks  :1202  spawn  Code
```

Data flows one direction: event source → interface → core → transport → messaging API → group chat. No bidirectional communication in Phase 1-2.

### Key Decisions
1. **Pluggable transport via Python Protocol** — The `Transport` protocol defines 3 methods (`send_message`, `create_group`, `health_check`). New transports require only implementing this interface. No changes to core, CLI, MCP, or skill code. Rationale: WhatsApp is blocked on Meta verification; Telegram ships immediately; we need both without duplication.

2. **File-based config, no database** — `~/.config/tool-telegram-whatsapp/config.json` stores credentials and project→group mapping. JSONL files for history. Rationale: ~400 lines of code shouldn't need SQLite or Postgres. Config changes are rare and can be edited by hand.

3. **CLI as the Afterburner integration point** — POST_MERGE_HOOKS shell out to `whatsup notify <slug> <event>`. Not HTTP, not MCP. Rationale: shell hooks are the simplest, most reliable integration. No daemon needs to be running. If the CLI is on PATH, it works.

4. **Sync core, async MCP wrapper** — `core.py` uses synchronous `requests`. The MCP server wraps calls with `asyncio.to_thread()`. Rationale: keeps the core simple and testable. MCP's async requirement doesn't need to infect the entire codebase.

5. **Telegram first, WhatsApp later** — Telegram Bot API is free, official, unlimited, instant setup. WhatsApp Business Cloud API requires Meta Business verification (days-weeks) and Official Business Account for Groups API. Rationale: ship something usable now, add WhatsApp when verification completes.

### Technical Constraints
- WhatsApp Groups API requires Official Business Account (green tick) — not guaranteed for solo developers
- WhatsApp outbound-first messages require pre-approved message templates
- Telegram groups require the bot to be added as a member before it can send messages
- Config file must not be committed to git (contains API tokens)
- MCP server runs via stdio (spawned by Claude Code) — cannot share state with REST server

### Tech Stack
- **Language:** Python 3.11+
- **HTTP client:** `requests` (sync, simple, no async overhead)
- **MCP framework:** `mcp` Python package (Anthropic's official MCP SDK)
- **CLI framework:** `argparse` (stdlib, zero dependencies)
- **REST server:** `http.server` (stdlib) or FastAPI (if auto-docs are desired)
- **Config format:** JSON (`~/.config/tool-telegram-whatsapp/config.json`)
- **History format:** JSONL (one JSON object per line, append-only)
- **Package manager:** pip with `pyproject.toml`
- **Transports:** Telegram Bot API (Phase 1), WhatsApp Business Cloud API (Phase 3)
