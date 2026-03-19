# whatsup

Per-project group-chat messaging for [Afterburner](https://github.com/anthropics/afterburner) sprints — Telegram, WhatsApp (planned), and a console transport for local testing.

<!-- badges placeholder -->
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

## What It Does

**whatsup** sends checkins and lifecycle notifications (sprint started, agent completed, tests failed, sprint merged) to the right project group chat automatically. It exposes four interfaces — CLI, REST API, MCP server, and a Claude skill — all backed by a single core module with pluggable transports.

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/davidbmar/tool-telegram-whatsapp.git
cd tool-telegram-whatsapp
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. Run setup — creates config, starts server, opens config UI
whatsup setup

# 3. Follow the setup guide at http://localhost:1202/config to connect Telegram

# 4. Send a message (after connecting Telegram)
whatsup send my-project "Hello from whatsup!"
```

> **Note:** Always activate the venv first: `source .venv/bin/activate`
> Or use `python3 cli.py` directly without a venv.

### Try it without Telegram first

The setup creates a **console transport** by default — messages print to stdout, no credentials needed:

```bash
whatsup send demo "hello from whatsup"    # prints to terminal
whatsup status                             # shows "console: OK"
```

### Connect to Telegram

The config UI at **http://localhost:1202/config** has a step-by-step setup guide. In short:

1. Message **@BotFather** on Telegram → `/newbot` → get a bot token
2. Disable privacy mode: `/mybots` → your bot → Bot Settings → Group Privacy → Turn off
3. Create a Telegram group, add the bot, send a message in the group
4. Get the group ID: `curl https://api.telegram.org/bot<TOKEN>/getUpdates | python3 -m json.tool`
5. In the config UI: paste token, set transport to telegram, paste group ID, Save, Send Test

See the full guide with troubleshooting at **http://localhost:1202/config**.

## Architecture

Four interfaces, one core:

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
│   CLI    │  │   REST   │  │   MCP    │  │ Claude Skill │
│ whatsup  │  │  :1202   │  │  stdio   │  │  /whatsup    │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘
     └─────────────┴──────┬──────┴────────────────┘
                    core.py
                          │
                  transport/ (pluggable)
               ┌──────┼──────────┐
           telegram  console  whatsapp
                              (planned)
```

Every interface calls `core.send()` or `core.notify()`. The core loads config, picks a transport, formats the message, and logs it to JSONL history.

## Configuration

Config lives at `~/.config/tool-telegram-whatsapp/config.json`. Run `whatsup init` to generate a starter file.

```jsonc
{
  "transports": {
    "telegram": {
      "botToken": "123456:ABC-DEF..."       // Telegram Bot API token
    },
    "whatsapp": {
      "phoneNumberId": "123456789",          // WhatsApp Business phone ID
      "accessToken": "EAA..."                // WhatsApp Cloud API token
    },
    "console": {}                            // No credentials needed
  },
  "projects": [
    {
      "slug": "demo",                        // Project identifier
      "transport": "console",                // Which transport to use
      "groupId": "demo-group",              // Chat/group ID for the transport
      "notify": [                            // Events that trigger notifications
        "sprint-started",
        "agent-completed",
        "sprint-merged",
        "test-failure",
        "checkin"
      ]
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `transports.<name>` | object | Credentials for each transport |
| `transports.telegram.botToken` | string | Telegram Bot API token from @BotFather |
| `transports.whatsapp.phoneNumberId` | string | WhatsApp Business phone number ID |
| `transports.whatsapp.accessToken` | string | WhatsApp Cloud API access token |
| `transports.console` | object | Empty — prints to stdout, no credentials |
| `projects[].slug` | string | Unique project identifier used in all commands |
| `projects[].transport` | string | Transport name (`telegram`, `console`, `whatsapp`) |
| `projects[].groupId` | string | Chat/group ID for the chosen transport |
| `projects[].notify` | array | Event types that trigger notifications |

### Supported events

`sprint-started`, `agent-completed`, `sprint-merged`, `test-failure`, `checkin`

## CLI Reference

### `whatsup send <slug> <message>`

Send a checkin message to a project's group chat.

```bash
whatsup send grassyknoll "Deployed auth service to staging"
```

### `whatsup notify <slug> <event> [options]`

Send a lifecycle notification. Only fires if the event is in the project's `notify` list.

```bash
whatsup notify grassyknoll sprint-merged --sprint 3 --status passed --summary "All tests green"
whatsup notify grassyknoll test-failure --sprint 3 --agent agentA --exit-code 1
```

| Option | Type | Description |
|--------|------|-------------|
| `--sprint` | int | Sprint number |
| `--status` | string | Test status (`passed` / `failed`) |
| `--summary` | string | Summary text |
| `--agent` | string | Agent name |
| `--exit-code` | int | Exit code |

### `whatsup projects`

List all configured projects.

```bash
whatsup projects
# Slug                 Transport    Group ID
# ────────────────────────────────────────────
# demo                 console      demo-group
# grassyknoll          telegram     -1001234567890
```

### `whatsup status`

Check transport health (verifies credentials / connectivity).

```bash
whatsup status
# telegram: OK
# console: OK
```

### `whatsup server [--port PORT]`

Start the REST API server (default port 1202).

```bash
whatsup server
whatsup server --port 8080
```

### `whatsup init`

Generate a sample config at `~/.config/tool-telegram-whatsapp/config.json` using the console transport so you can test without credentials.

```bash
whatsup init
# Created config at ~/.config/tool-telegram-whatsapp/config.json
```

## REST API Reference

Default: `http://localhost:1202`. Set port with `--port` or `WHATSUP_PORT` env var.

### `POST /send`

```bash
curl -X POST http://localhost:1202/send \
  -H "Content-Type: application/json" \
  -d '{"slug": "demo", "message": "hello from REST"}'
```

```json
{"ok": true, "data": {"ok": true, "message_id": "..."}}
```

### `POST /notify`

```bash
curl -X POST http://localhost:1202/notify \
  -H "Content-Type: application/json" \
  -d '{"slug": "demo", "event": "sprint-merged", "sprint": 3, "status": "passed"}'
```

```json
{"ok": true, "data": {"ok": true, "message_id": "..."}}
```

### `GET /projects`

```bash
curl http://localhost:1202/projects
```

```json
{"ok": true, "data": [{"slug": "demo", "transport": "console", "groupId": "demo-group", "notify": ["sprint-merged"]}]}
```

### `GET /status`

```bash
curl http://localhost:1202/status
```

```json
{"ok": true, "data": {"console": {"ok": true}, "telegram": {"ok": true}}}
```

### `GET /history?slug=<slug>&limit=20`

```bash
curl "http://localhost:1202/history?slug=demo&limit=5"
```

```json
{"ok": true, "data": [{"timestamp": "...", "direction": "outbound", "event": "send", "message": "..."}]}
```

## MCP Server

Register in your `.mcp.json`:

```json
{
  "mcpServers": {
    "tool-telegram-whatsapp": {
      "command": "python",
      "args": ["-m", "whatsup.mcp_server"],
      "cwd": "/path/to/tool-telegram-whatsapp"
    }
  }
}
```

### Available tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `send_checkin` | Send a checkin to a project's group chat | `slug`, `summary`, `details?` |
| `send_notification` | Send a sprint lifecycle notification | `slug`, `event`, `sprint?`, `status?`, `summary?` |
| `whatsup_projects` | List projects with messaging configured | _(none)_ |
| `whatsup_status` | Check transport connection status | _(none)_ |

## Claude Skill

The `/whatsup` skill lets you send messages from Claude Code:

```
/whatsup grassyknoll Deployed auth service to staging
/whatsup status
/whatsup projects
```

Install the skill by copying `skills/whatsup.md` to your Claude skills directory:

```bash
cp skills/whatsup.md ~/.claude/skills/
```

## Security

The server binds to **127.0.0.1** by default — it is not accessible from the network.

### Config write protection

Set `WHATSUP_API_TOKEN` to require a token on `POST /api/config`:

```bash
export WHATSUP_API_TOKEN=mysecret
whatsup server
```

Requests must then include the token via header or query parameter:

```bash
# Header
curl -X POST http://localhost:1202/api/config \
  -H "Content-Type: application/json" \
  -H "X-Whatsup-Token: mysecret" \
  -d '{ ... }'

# Query parameter
curl -X POST "http://localhost:1202/api/config?token=mysecret" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

If `WHATSUP_API_TOKEN` is not set (the default), no token is required — localhost-only access is considered acceptable.

### Remote access

Set `WHATSUP_BIND=0.0.0.0` only if you need remote access (**not recommended**). If you do, always set `WHATSUP_API_TOKEN` as well:

```bash
export WHATSUP_BIND=0.0.0.0
export WHATSUP_API_TOKEN=mysecret
whatsup server
```

## Transports

| Transport | Status | Use case |
|-----------|--------|----------|
| **console** | Available | Local testing and demos — prints to stdout |
| **telegram** | Available | Production — sends via Telegram Bot API |
| **whatsapp** | Planned | WhatsApp Business Cloud API |

The console transport requires no credentials and is configured by default when you run `whatsup init`.

## Afterburner Integration

whatsup integrates with Afterburner sprints via `POST_MERGE_HOOKS` in `.sprint/config.sh`:

```bash
POST_MERGE_HOOKS=(
  "whatsup notify \$PROJECT_SLUG sprint-merged --sprint \$SPRINT --status \$STATUS --summary \"\$SUMMARY\""
)
```

This fires a notification to the project's group chat after each sprint merge. Events like `sprint-started` and `agent-completed` can also be wired to sprint lifecycle scripts.

## Development

### Run tests

```bash
pip install -e ".[dev]"
pytest
```

### Project structure

```
cli.py                  CLI entry point (whatsup command)
whatsup/
  __init__.py           Package version
  core.py               Business logic — send, notify, projects, status
  config.py             Config loader (~/.config/tool-telegram-whatsapp/)
  messages.py           Event formatters (5 event types)
  server.py             REST API server (port 1202)
  mcp_server.py         MCP server (stdio, 4 tools)
  history.py            JSONL message history
  transport/
    __init__.py          Transport protocol
    telegram.py          Telegram Bot API transport
skills/
  whatsup.md            Claude skill definition
```

## License

MIT
