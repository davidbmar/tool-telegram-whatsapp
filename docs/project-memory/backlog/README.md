# Backlog

Track bugs and feature requests for tool-telegram-whatsapp.

## Bugs

| ID | Title | Priority | Status |
|----|-------|----------|--------|
| B-001 | MCP server fails to import — `mcp` package not installed in system Python | High | Done (Sprint 4) |
| B-002 | REST server handler class is private (`_Handler`) — not importable by name | Low | Done (Sprint 4) |
| B-003 | CLI `projects` and `status` crash with unhelpful traceback when config missing | Medium | Done (Sprint 3) |
| B-004 | `python3 whatsup/server.py` fails with ModuleNotFoundError — needs `__main__.py` | Medium | Done (Sprint 4) |
| B-005 | Skill file says `python -m` instead of `python3 -m` on entry point line | Low | Done (Sprint 4) |
| B-006 | README clone URL says `yourorg` instead of `davidbmar` | Low | Done (Sprint 4) |
| B-007 | Server binds to 0.0.0.0 — exposes config UI and API to entire network | High | Done (hotfix) |
| B-008 | `/status` and `/projects` endpoints return raw JSON — no HTML for browsers | Medium | Open |
| B-009 | `/api/config` POST has no authentication — anyone on localhost can overwrite config | Medium | Open |

## Features

| ID | Title | Priority | Status |
|----|-------|----------|--------|
| F-001 | Test suite — pytest tests for core, messages, config, history, CLI | High | Done (Sprint 3) |
| F-002 | Sample config + `whatsup init` command to generate config template | High | Done (Sprint 3) |
| F-003 | Install skill to ~/.claude/skills/ via `whatsup install-skill` | Medium | Done (Sprint 4) |
| F-004 | `python3 -m whatsup.server` entry point for running REST server as module | Medium | Done (Sprint 3) |
| F-005 | `GET /schema` endpoint on REST server for tool plugin system | Medium | Done (Sprint 4) |
| F-006 | `whatsup register` command to self-register in Afterburner tool registry | Medium | Deferred |
| F-007 | README.md rewrite — installation, quickstart, config reference, API docs | High | Done (Sprint 3) |
| F-008 | `tool_config.py` — Afterburner per-project config reader (reference impl) | Medium | Deferred |
| F-009 | Console transport for testing without Telegram — prints to stdout | Medium | Done (Sprint 3) |
| F-010 | `whatsup/` package `__main__.py` for `python3 -m whatsup` entry point | Medium | Done (Sprint 4) |
| F-011 | REST server: add `GET /history` endpoint docs to README | Low | Done (Sprint 3) |
| F-012 | pip install -e . in venv should be part of quickstart in README | Low | Done |
| F-013 | Config UI: auto-collapse setup guide once Telegram is connected | Low | Open |
| F-014 | HTML views for /status and /projects when accessed from browser | Medium | Open |

## Summary

- **All critical bugs closed** (7/9 done, 2 medium open)
- **Features done**: 12/14
- **Open items**: B-008 (HTML views), B-009 (config auth), F-013 (auto-collapse guide), F-014 (HTML views)
