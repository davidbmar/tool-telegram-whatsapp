# Session

Session-ID: S-2026-03-19-0433-console-transport-init
Title: Add console transport and whatsup init command
Date: 2026-03-19
Author: agentA

## Goal

Add a console transport for testing without Telegram credentials and a `whatsup init` command to generate sample config.

## Context

Sprint 3 task. The tool previously required Telegram credentials for any usage. A console transport enables local testing and demos.

## Plan

1. Create `whatsup/transport/console.py` with ConsoleTransport class
2. Wire it into `core.py` factory function
3. Add `init` subcommand to `cli.py`
4. Add pytest dev dependency to pyproject.toml

## Changes Made

- Created `whatsup/transport/console.py` — ConsoleTransport implementing the Transport protocol
- Updated `whatsup/core.py` — added console case to `_get_transport()`, imported ConsoleTransport
- Updated `cli.py` — added `init` subcommand that creates sample config with console transport
- Updated `pyproject.toml` — added `[project.optional-dependencies]` with `dev = ["pytest"]`

## Decisions Made

- **Config format**: The brief's sample config showed `projects` as a dict keyed by slug, but existing `config.py` expects a list with `slug` fields. Used list format to maintain backward compatibility with existing code.
- **No import of `Path`**: Reused `CONFIG_PATH` from `whatsup.config` rather than duplicating the path logic.

## Open Questions

None.

## Links

Commits:
- (pending)
