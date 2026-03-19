agentC-readme-docs — Sprint 3

Previous Sprint Summary
─────────────────────────────────────────
- Sprint 2 shipped: REST API server on :1202, sprint-started + agent-completed formatters, real core.py business logic, JSONL history, .gitignore
- Known issues: MCP server can't import (`mcp` package not in system Python), no test suite, no sample config, README is scaffolding only
─────────────────────────────────────────

Sprint-Level Context

Goal
- Add comprehensive test suite so the tool is independently testable
- Fix MCP server dependency and make all interfaces work out of the box
- Add `whatsup init` command to generate sample config
- Add console transport for testing without Telegram credentials
- Write proper README.md with installation, quickstart, and API docs

Constraints
- Python 3.11+, use `python3` in all commands
- Tests use pytest — add `pytest` to dev dependencies in pyproject.toml
- Console transport prints to stdout instead of calling Telegram API — useful for testing and demos
- `whatsup init` creates `~/.config/tool-telegram-whatsapp/config.json` with a sample config using console transport
- README must be GitHub-ready with badges, installation, quickstart, config reference, and interface docs
- Agents run non-interactively — MUST NOT ask for confirmation or approval
- Existing imports must not break


Objective
- Write a comprehensive README.md for the GitHub repo

Tasks
- Rewrite `README.md` at repo root (~150 lines) with these sections:
  - **Header**: project name, one-line description, badges placeholder
  - **What It Does**: 2-3 sentences explaining the tool — per-project messaging for Afterburner sprints via Telegram/WhatsApp
  - **Quick Start**: 5 steps — clone, pip install -e, whatsup init, whatsup send demo "hello", see output
  - **Architecture**: the "four interfaces, one core" diagram from the design docs
  - **Configuration**: full config.json reference with all fields documented
  - **CLI Reference**: all subcommands with usage examples (send, notify, projects, status, server, init)
  - **REST API Reference**: all endpoints with request/response examples
  - **MCP Server**: how to register in .mcp.json, available tools
  - **Claude Skill**: how /whatsup works
  - **Transports**: console (for testing), telegram (for production), whatsapp (planned)
  - **Afterburner Integration**: how POST_MERGE_HOOKS wiring works
  - **Development**: how to run tests, project structure
  - **License**: MIT
- Install `skills/whatsup.md` — add a note in README about copying it to `~/.claude/skills/`

Acceptance Criteria
- README.md at repo root is >100 lines with all sections listed above
- Quick Start section works if followed literally (clone → init → send demo)
- Config reference documents every field in config.json
- All 5 CLI subcommands are documented with examples
