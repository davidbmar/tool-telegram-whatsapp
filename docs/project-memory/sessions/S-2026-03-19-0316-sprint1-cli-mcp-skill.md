# Session

Session-ID: S-2026-03-19-0316-sprint1-cli-mcp-skill
Title: Sprint 1 — CLI, MCP server, and Claude skill
Date: 2026-03-19
Author: agentC

## Goal

Create the CLI entry point (`cli.py`), MCP server (`whatsup/mcp_server.py`), and Claude skill file (`skills/whatsup.md`) for the whatsup messaging tool.

## Context

Sprint 1 multi-agent build. Agent A creates transport/config layer, agent B creates core/messages, agent C (this session) creates interface layer. Merge order: A → B → C.

## Plan

1. Create `cli.py` with argparse subcommands: send, notify, projects, status
2. Create `whatsup/mcp_server.py` with FastMCP tools wrapping core functions
3. Create `skills/whatsup.md` with skill definition and MCP tool mappings
4. Create stub `whatsup/core.py` and `whatsup/messages.py` so imports work pre-merge

## Changes Made

- `cli.py` — argparse CLI with send, notify, projects, status subcommands
- `whatsup/mcp_server.py` — FastMCP server with 4 tools (send_checkin, send_notification, whatsup_projects, whatsup_status)
- `skills/whatsup.md` — Claude skill definition with trigger patterns and MCP tool mapping
- `whatsup/__init__.py` — package init (will be superseded by agent A's version at merge)
- `whatsup/core.py` — stub core module (will be superseded by agent B's version at merge)
- `whatsup/messages.py` — stub messages module (will be superseded by agent B's version at merge)

## Decisions Made

- Used `FastMCP` (from `mcp.server.fastmcp`) instead of lower-level `Server` class — simpler decorator-based API, fewer lines of code
- Created stub core.py and messages.py with real implementations matching the spec so acceptance tests pass in isolation; these will be replaced by agent B's versions at merge
- CLI uses lazy imports in core.py (config, transport) to defer missing-dependency errors to runtime rather than import time

## Open Questions

- Merge conflicts on `whatsup/__init__.py`, `core.py`, `messages.py` expected — agent A/B versions should take precedence

## Links

Commits:
- (pending)
