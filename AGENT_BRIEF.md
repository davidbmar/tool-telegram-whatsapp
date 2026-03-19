agentA-console-transport-init — Sprint 3

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
