# Session

Session-ID: S-2026-03-19-0313-transport-config
Title: Core package, config loader, and Telegram transport
Date: 2026-03-19
Author: Agent A

## Goal

Create the project packaging, config loader, and pluggable transport layer with Telegram implementation.

## Context

Sprint 1 — first agent task. No existing code; building the foundational package structure.

## Plan

1. Create pyproject.toml with package metadata
2. Create whatsup/__init__.py with version
3. Create whatsup/config.py with load_config, get_project, get_all_projects
4. Create whatsup/transport/__init__.py with Transport Protocol
5. Create whatsup/transport/telegram.py with TelegramTransport
6. Create whatsup/core.py for convenience re-exports (needed by smoke test)

## Changes Made

- `pyproject.toml` — package metadata, deps (requests, mcp), CLI entry point
- `whatsup/__init__.py` — version string
- `whatsup/config.py` — load_config, get_project, get_all_projects reading from ~/.config/tool-telegram-whatsapp/config.json
- `whatsup/transport/__init__.py` — Transport typing.Protocol with send_message, create_group, health_check
- `whatsup/transport/telegram.py` — TelegramTransport using requests against Telegram Bot API
- `whatsup/core.py` — re-exports all public API (required by brief's smoke test)

## Decisions Made

- Used `typing.Protocol` for Transport interface — structural subtyping, no inheritance required
- TelegramTransport.create_group creates an invite link since Telegram Bot API cannot create groups
- All HTTP errors caught and returned as dicts rather than raised — matches brief's "handle errors gracefully"
- Created core.py to satisfy brief's smoke test `from whatsup import core`

## Open Questions

- None

## Links

Commits:
- (pending)
