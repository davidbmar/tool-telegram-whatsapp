# Sprint 4 — Agent Notes

*Started: 2026-03-19 04:45 UTC*

Phase 1 Agents: 2
- agentA-bugfixes
- agentB-schema-skill

Phase 2 Agents: 0
(none)

Automated summaries from each agent are appended below as they complete.

---

## agentB-schema-skill

*Completed: 2026-03-19 04:49 UTC*

## Files changed
- **`whatsup/server.py`** — Added `GET /schema` endpoint returning JSON Schema with `tool`, `version`, `globalConfig`, `projectConfig`
- **`cli.py`** — Added `install-skill` subcommand that copies `skills/whatsup.md` to `~/.claude/skills/whatsup.md`
- **`tests/test_server.py`** — New file with 7 tests for `/schema` endpoint (tool name, version, properties, enums, required fields, sensitive flag)
- **`tests/test_cli.py`** — Added `test_cli_install_skill` test
- **`pyproject.toml`** — Fixed invalid build-backend (`setuptools.backends._legacy:_Backend` → `setuptools.build_meta`), added package discovery config
- **`docs/project-memory/sessions/S-2026-03-19-0448-schema-install-skill.md`** — Session doc

## Commands run
- `python3.12 -m venv .venv && pip install -e ".[dev]"` — set up dev environment
- `.venv/bin/python -m pytest tests/ -v` — **35 tests passed** (8 new)
- `git push -u origin HEAD` — branch pushed

## Notes / follow-on work
- The pyproject.toml had an invalid build-backend (`setuptools.backends._legacy:_Backend`) — fixed as part of this work
- Schema endpoint returns raw schema (not wrapped in `{"ok": true, "data": ...}`) to match the brief's expected curl output format


---

## agentA-bugfixes

*Completed: 2026-03-19 04:49 UTC*

## Files changed
- `whatsup/mcp_server.py` — B-001: MCP import wrapped in try/except with stub fallback
- `whatsup/server.py` — B-002: `_Handler` renamed to `WhatsupHandler`
- `whatsup/__main__.py` — B-004/F-010: New file, enables `python3 -m whatsup`
- `skills/whatsup.md` — B-005: `python` → `python3` in entry point
- `README.md` — B-006: `yourorg` → `davidbmar` in clone URL
- `pyproject.toml` — Fixed build backend (`setuptools.build_meta`), made `mcp` optional, added explicit package list
- `docs/project-memory/sessions/S-2026-03-19-0448-sprint4-bugfixes.md` — Session doc

## Commands run
- `python3.12 -m venv .venv` + `pip install -e ".[dev]"` — set up environment
- `.venv/bin/python -m pytest tests/ -v` — **27/27 tests passed**
- All 7 acceptance criteria verified successfully

## Notes / follow-on work
- The original `pyproject.toml` had a broken build backend (`setuptools.backends._legacy:_Backend`) — fixed to `setuptools.build_meta`
- `mcp` moved from hard dependency to optional (`pip install whatsup[mcp]`) to support graceful degradation

