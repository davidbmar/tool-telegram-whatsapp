# Session

Session-ID: S-2026-03-19-0408-sprint2-events-history
Title: Sprint 2 — New event formatters, core business logic, JSONL history
Date: 2026-03-19
Author: agentB

## Goal

Add sprint-started and agent-completed event types, rewrite core.py with real business logic (send/notify/projects/status), and add JSONL message history logging per project.

## Context

Sprint 1 shipped config, transport, messages (3 formatters), MCP server, and CLI. However core.py only had re-exports — the MCP server inlined logic. This sprint wires up real business logic so the MCP tools work end-to-end.

## Plan

1. Add format_sprint_started and format_agent_completed to messages.py
2. Create whatsup/history.py with JSONL log_message/get_history
3. Rewrite core.py with send, notify, projects, status functions
4. Verify all acceptance criteria pass

## Changes Made

- `whatsup/messages.py` — added format_sprint_started, format_agent_completed, registered in _FORMATTERS
- `whatsup/history.py` — new file with log_message (JSONL append) and get_history (tail N lines)
- `whatsup/core.py` — rewritten with send(), notify(), projects(), status(), _get_transport() helper; kept backward-compat re-exports

## Decisions Made

- Used stdlib pathlib + json for history (no new dependencies)
- History stored at ~/.config/tool-telegram-whatsapp/history/{slug}.jsonl per brief spec
- notify() returns {"skipped": True, "reason": "..."} when event not in project's notify list
- send() logs every outbound message to history automatically

## Open Questions

- None

## Links

Commits:
- (pending)
