# Session

Session-ID: S-2026-03-19-0448-schema-install-skill
Title: Add /schema endpoint and install-skill CLI command
Date: 2026-03-19
Author: agentB

## Goal

Add GET /schema endpoint to REST server and `whatsup install-skill` CLI command per Sprint 4 brief.

## Context

Sprint 4 — F-005 (schema endpoint) and F-003 (install-skill) from backlog. Afterburner dashboard needs schema endpoint to render config forms (F-017 in Afterburner backlog).

## Plan

1. Add /schema route to server.py returning JSON Schema for tool config
2. Add install-skill subcommand to cli.py
3. Add tests for both features
4. Fix pyproject.toml build backend issue encountered during setup

## Changes Made

- `whatsup/server.py`: Added `GET /schema` endpoint returning JSON Schema with tool name, version, globalConfig, and projectConfig
- `cli.py`: Added `install-skill` subcommand that copies `skills/whatsup.md` to `~/.claude/skills/whatsup.md`
- `tests/test_server.py`: New file with 7 tests for the /schema endpoint
- `tests/test_cli.py`: Added `test_cli_install_skill` test
- `pyproject.toml`: Fixed build-backend and added package discovery config

## Decisions Made

- Schema endpoint returns the schema directly (not wrapped in `{"ok": true, "data": ...}`) to match the brief's expected output format
- install-skill overwrites without prompting (non-interactive mode per brief)
- Fixed pyproject.toml build-backend from invalid `setuptools.backends._legacy:_Backend` to `setuptools.build_meta`

## Open Questions

None.

## Links

Commits:
- (pending)
