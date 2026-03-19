# PROJECT STATUS — tool-telegram-whatsapp (Sprint 1)

**Date:** 2026-03-19
**Sprint:** 1
**Project:** tool-telegram-whatsapp

## Sprint 1 Summary

Built the core `whatsup` Python package with pluggable transport layer, Telegram Bot API as the first transport, CLI and MCP server interfaces, and a Claude skill for conversational use. All 3 agents completed and merged successfully. End-to-end imports verified.

---

## Merge Table

| # | Branch | Deliverable | Phase | Conflicts |
|---|--------|-------------|-------|-----------|
| 1 | agentA-transport-config | Package setup, config loader, Transport protocol, Telegram client | 1 | Clean |
| 2 | agentB-core-messages | Core business logic (send/notify/projects/status) + message formatters | 1 | Clean |
| 3 | agentC-cli-mcp-skill | CLI entry point, MCP server (4 tools), Claude skill definition | 1 | Ephemeral only |

## What Changed

### Package & Config
- `pyproject.toml` — package metadata, deps (`requests`, `mcp`), CLI entry point
- `whatsup/__init__.py` — `__version__ = "0.1.0"`
- `whatsup/config.py` — `load_config()`, `get_project()`, `get_all_projects()` reading from `~/.config/tool-telegram-whatsapp/config.json`

### Transport Layer
- `whatsup/transport/__init__.py` — `Transport` Protocol class (3 methods: `send_message`, `create_group`, `health_check`)
- `whatsup/transport/telegram.py` — `TelegramTransport` implementing Bot API (`sendMessage`, `getMe`, `createChatInviteLink`)

### Core & Messages
- `whatsup/core.py` — `send()`, `notify()`, `projects()`, `status()` with event filtering per project config
- `whatsup/messages.py` — `format_checkin`, `format_sprint_merged`, `format_test_failure`, `format_event` dispatcher

### Interfaces
- `cli.py` — argparse CLI with `send`, `notify`, `projects`, `status` subcommands
- `whatsup/mcp_server.py` — FastMCP server with 4 tools (`send_checkin`, `send_notification`, `whatsup_projects`, `whatsup_status`)
- `skills/whatsup.md` — Claude skill definition for `/whatsup` command

## Capabilities

- Transport-agnostic messaging with pluggable backend protocol
- Per-project group routing via config file
- Event filtering — each project subscribes to specific notification types
- Four interfaces (CLI, REST planned, MCP, skill) sharing one core

## Next Steps

1. Sprint 2: REST API on port 1202
2. Sprint 2: Wire Afterburner POST_MERGE_HOOKS integration
3. Sprint 2: Add sprint-started and agent-completed event types
4. Sprint 2: JSONL message history logging
5. Sprint 3: WhatsApp Business Cloud API transport

## Known Issues

- `__pycache__` files accidentally committed (need `.gitignore`)
- Sprint verification used `python` instead of `python3` — fixed in Afterburner framework

## Sessions

- S-2026-03-19-0313-transport-config
- S-2026-03-19-0314-sprint1-core-messages
- S-2026-03-19-0316-sprint1-cli-mcp-skill
