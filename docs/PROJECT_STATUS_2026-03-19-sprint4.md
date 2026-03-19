# PROJECT STATUS — tool-telegram-whatsapp (Sprint 4)

**Date:** 2026-03-19
**Sprint:** 4
**Project:** tool-telegram-whatsapp

## Sprint 4 Summary

Production readiness sprint: fixed all open bugs (MCP optional import, __main__.py, handler rename, skill typo, README URL), added /schema endpoint for Afterburner tool plugin integration, added `whatsup install-skill` command. Test suite grew from 27 to 35 tests.

---

## Merge Table

| # | Branch | Deliverable | Phase | Conflicts |
|---|--------|-------------|-------|-----------|
| 1 | agentA-bugfixes | Fixed B-001 through B-006: MCP optional, __main__.py, WhatsupHandler, skill/README fixes | 1 | Clean |
| 2 | agentB-schema-skill | GET /schema endpoint (JSON Schema for plugin system), `whatsup install-skill` CLI, 7 new server tests | 1 | Clean |

## What Changed

### Bug Fixes
- B-001: MCP import is now optional — tool works without `mcp` package, graceful error message
- B-002: `_Handler` renamed to `WhatsupHandler` — publicly importable
- B-004: `whatsup/__main__.py` added — `python3 -m whatsup` works
- B-005: Skill file corrected to use `python3`
- B-006: README clone URL fixed to `davidbmar`

### Schema Endpoint
- `GET /schema` returns JSON Schema with `globalConfig` and `projectConfig` — ready for Afterburner dashboard integration (F-017)
- Schema includes transport enum, groupId, notify array with event types

### Install Skill
- `whatsup install-skill` copies `skills/whatsup.md` to `~/.claude/skills/`
- Creates directory if needed

### pyproject.toml
- `mcp` moved to optional dependency: `pip install whatsup[mcp]`
- `setuptools` build backend fixed

## Test Results

35 tests, all passed (4.00s)

## Backlog Status

| ID | Status |
|----|--------|
| B-001 through B-006 | All Done |
| F-001, F-002, F-004, F-007, F-009 | Done (Sprint 3) |
| F-003 (install-skill) | Done (Sprint 4) |
| F-005 (/schema) | Done (Sprint 4) |
| F-006 (register), F-008 (tool_config) | Open — defer to when Afterburner tool registry is built |
| F-010 (__main__) | Done (Sprint 4) |
| F-011, F-012 | Open — low priority docs polish |

## Next Steps

1. Wire POST_MERGE_HOOKS in a real Afterburner project (use console transport for testing)
2. Set up Telegram bot for live messaging
3. Build tool_config.py when Afterburner tool registry (F-016) ships
