# Session

Session-ID: S-2026-03-19-0604-sprint5-config-polish
Title: Sprint 5 — Config UI polish and endpoint protection
Date: 2026-03-19
Author: agentB

## Goal

Auto-collapse setup guide when Telegram is configured, add token-based protection to POST /api/config, and add Security section to README.

## Context

Sprint 5 brief tasks for agentB: config polish. The setup guide is always expanded even when the user has already connected Telegram. The /api/config POST endpoint has no auth, which could allow accidental writes.

## Plan

1. Modify config_ui.html — detect configured Telegram projects, auto-collapse guide, add "Show setup guide" link
2. Modify server.py — add WHATSUP_API_TOKEN check on POST /api/config
3. Update README.md — add Security section
4. Add tests for token auth
5. Run tests, commit, push

## Changes Made

- `whatsup/config_ui.html`: Added `toggleGuide()`, `collapseGuide()`, `hasTelegramConfigured()` functions. The `load()` function now auto-collapses the setup guide when any project has `transport: "telegram"` with a non-empty `groupId`. Added a "Show setup guide" link that appears when collapsed.
- `whatsup/server.py`: Added `_check_config_token()` method that reads `WHATSUP_API_TOKEN` env var. When set, `POST /api/config` requires the token via `X-Whatsup-Token` header or `token` query param. Returns 403 if missing/wrong. When unset, no auth required.
- `README.md`: Added Security section documenting 127.0.0.1 binding, `WHATSUP_API_TOKEN` for config write protection, and `WHATSUP_BIND` warning.
- `tests/test_server.py`: Added 5 tests for token auth (no token env allows, missing token rejects, wrong token rejects, header auth works, query param auth works).

## Decisions Made

- Used Unicode characters (`\u25BC`, `\u25B6`) instead of `innerHTML` with HTML entities to avoid XSS risk flagged by security hook.
- Token check happens before any file I/O in `_handle_config_save` (fail fast).
- Token can be passed via header or query param for flexibility (curl vs browser).

## Open Questions

None.

## Links

Commits:
- (see branch agentB-config-polish)

PRs:
- (pending)
