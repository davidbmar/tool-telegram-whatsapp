# Sprint 3

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

Merge Order
1. agentA-console-transport-init
2. agentB-tests
3. agentC-readme-docs

Merge Verification
- python3 -m pytest tests/ -v

Previous Sprint
- Sprint 2 shipped: REST API server on :1202, sprint-started + agent-completed formatters, real core.py business logic, JSONL history, .gitignore
- Known issues: MCP server can't import (`mcp` package not in system Python), no test suite, no sample config, README is scaffolding only

## agentA-console-transport-init

Objective
- Add a console transport for testing without credentials and a `whatsup init` command to generate sample config

Tasks
- Create `whatsup/transport/console.py` (~30 lines):
  - Class `ConsoleTransport` implementing the Transport protocol
  - `send_message(group_id, text)` — prints `"[whatsup → {group_id}] {text}"` to stdout, returns `{"ok": True, "transport": "console"}`
  - `create_group(name, members)` — prints creation message, returns `"console-group-{name}"`
  - `health_check()` — returns `{"ok": True, "transport": "console", "mode": "local"}`
- Update `whatsup/core.py`:
  - In `_get_transport()`, add `"console"` case that returns `ConsoleTransport()`
- Add `init` subcommand to `cli.py`:
  - `whatsup init` — creates `~/.config/tool-telegram-whatsapp/config.json` if it doesn't exist
  - Sample config uses `"console"` transport so it works immediately without credentials:
    ```json
    {
      "transports": {
        "console": {},
        "telegram": {"botToken": "YOUR_BOT_TOKEN_HERE"}
      },
      "projects": {
        "demo": {
          "transport": "console",
          "groupId": "demo-group",
          "notify": ["sprint-merged", "test-failure", "checkin", "sprint-started", "agent-completed"]
        }
      }
    }
    ```
  - If config already exists, print "Config already exists at ..." and exit without overwriting
  - After creating, print "Config created. Test with: whatsup send demo 'Hello world'"
- Update `pyproject.toml`:
  - Add `pytest` to `[project.optional-dependencies]` dev group: `dev = ["pytest"]`
  - Ensure `mcp` is listed in main dependencies (it should already be there)

Acceptance Criteria
- `from whatsup.transport.console import ConsoleTransport` imports without error
- `ConsoleTransport().send_message("test", "hello")` prints to stdout and returns dict
- `python3 cli.py init` creates config file at expected path
- After init, `python3 cli.py send demo "Hello world"` works (prints to console, no Telegram needed)
- After init, `python3 cli.py projects` shows the demo project
- After init, `python3 cli.py status` shows console transport healthy

## agentB-tests

Objective
- Create a comprehensive pytest test suite covering core, messages, config, history, and CLI

Tasks
- Create `tests/` directory with `__init__.py`
- Create `tests/conftest.py` (~30 lines):
  - Fixture `tmp_config` — creates a temporary config.json with console transport + demo project, sets env var or monkeypatches config path
  - Fixture `clean_history` — creates a temporary history directory
- Create `tests/test_messages.py` (~50 lines):
  - Test each of the 5 formatters returns correct strings
  - Test `format_event` dispatches correctly
  - Test `format_event` raises ValueError for unknown events
- Create `tests/test_config.py` (~40 lines):
  - Test `load_config` reads JSON file
  - Test `load_config` raises FileNotFoundError with helpful message when missing
  - Test `get_project` returns correct project
  - Test `get_project` raises ValueError for unknown slug
  - Test `get_all_projects` returns list
- Create `tests/test_core.py` (~50 lines):
  - Test `send()` with console transport — should succeed and return result
  - Test `notify()` with event in notify list — should send
  - Test `notify()` with event NOT in notify list — should return skipped
  - Test `projects()` returns list of projects
  - Test `status()` returns health check dict
- Create `tests/test_history.py` (~30 lines):
  - Test `log_message` creates JSONL file and appends
  - Test `get_history` reads back logged messages
  - Test `get_history` with limit
- Create `tests/test_cli.py` (~40 lines):
  - Test `whatsup --help` exits 0
  - Test `whatsup send demo "hello"` works with console transport
  - Test `whatsup projects` shows demo project
  - Test `whatsup status` shows console healthy
  - Use `subprocess.run` to test CLI as external process
- Note: all tests should use the console transport and temporary config — no Telegram credentials needed

Acceptance Criteria
- `python3 -m pytest tests/ -v` runs and all tests pass
- At least 15 tests covering messages, config, core, history, and CLI
- No tests require network access or real Telegram credentials

## agentC-readme-docs

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
