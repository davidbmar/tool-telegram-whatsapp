# Session

Session-ID: S-2026-03-19-0314-sprint1-core-messages
Title: Sprint 1 — Core business logic and message formatting
Date: 2026-03-19
Author: agentB

## Goal

Implement `whatsup/messages.py` and `whatsup/core.py` as part of Sprint 1 multi-agent work.

## Context

Sprint 1 multi-agent sprint. agentA creates transport/config (merges first), agentB (this agent) creates core/messages, agentC creates CLI/MCP.

## Plan

1. Create stub files for agentA dependencies (config, transport) so imports work in isolation
2. Implement `whatsup/messages.py` with all format functions
3. Implement `whatsup/core.py` with send, notify, projects, status
4. Run acceptance criteria smoke tests

## Changes Made

- Created `whatsup/__init__.py` (stub, will be replaced by agentA)
- Created `whatsup/config.py` (stub, will be replaced by agentA)
- Created `whatsup/transport/__init__.py` (stub, will be replaced by agentA)
- Created `whatsup/transport/telegram.py` (stub, will be replaced by agentA)
- Created `whatsup/messages.py` — format_checkin, format_sprint_merged, format_test_failure, format_event
- Created `whatsup/core.py` — send, notify, projects, status, _get_transport

## Decisions Made

- Created stub files for agentA's dependencies so smoke tests pass in this branch. These will be overwritten when agentA merges first per merge order.
- Used a `_FORMATTERS` dict dispatch pattern in messages.py for the format_event dispatcher — clean and extensible.
- `notify()` checks the project's notify list and returns `{"skipped": True}` if event not enabled, matching the brief exactly.

## Open Questions

None — straightforward implementation per brief.

## Links

Commits:
- (pending)
