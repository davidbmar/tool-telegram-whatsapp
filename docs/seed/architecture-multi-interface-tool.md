# Building a Multi-Interface Tool: MCP, REST, CLI, and Claude Skill

## The Pattern

tool-telegram-whatsapp follows a "one core, many interfaces" architecture. The same business logic is exposed through four different interfaces, each serving a different consumer:

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
│   CLI    │  │   REST   │  │   MCP    │  │ Claude Skill │
│ whatsup  │  │ :1202    │  │ stdio    │  │ /whatsup     │
│ send ... │  │ /send    │  │ tools    │  │ (calls MCP)  │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘
     │             │             │                │
     └─────────────┴──────┬──────┴────────────────┘
                          │
                    core.py (business logic)
                          │
                    transport/ (pluggable)
                     ┌─────┴─────┐
                 telegram.py  whatsapp.py
```

## Why Four Interfaces?

### 1. CLI (`cli.py`)
**Consumer:** Shell scripts, cron jobs, Afterburner sprint hooks
**Why:** The POST_MERGE_HOOKS system in Afterburner shells out to commands. A CLI entry point means zero coupling — Afterburner just runs `whatsup notify grassyknoll sprint-merged ...`. Also useful for manual testing and ad-hoc messages.

**Pattern:** argparse with subcommands. Installable via `pip install -e .` with `[project.scripts]` in pyproject.toml.

```bash
whatsup send <project> <message>
whatsup notify <project> <event> [--sprint N] [--status S] [--summary S]
whatsup projects
whatsup status
```

### 2. REST API (`server.py`)
**Consumer:** Other services, webhooks, dashboard integrations
**Why:** HTTP is the universal integration protocol. The Afterburner dashboard could embed a WhatsApp/Telegram status panel by calling these endpoints. External CI/CD systems can POST notifications.

**Pattern:** Lightweight HTTP server (stdlib `http.server` or FastAPI). Standalone process on its own port (1202). JSON request/response.

```
POST /send         — {slug, message}
POST /notify       — {slug, event, sprint, status, summary}
GET  /projects     — list configured projects
GET  /status       — transport health
```

### 3. MCP Server (`mcp_server.py`)
**Consumer:** Claude Code and other LLM agents
**Why:** MCP (Model Context Protocol) is the standard for giving AI agents tool access. Registering tool-telegram-whatsapp as an MCP server means Claude Code can send messages, check status, and list projects without shelling out.

**Pattern:** Uses the `mcp` Python package. Runs via stdio (Claude Code spawns it). Each tool is a decorated async function.

```python
@mcp.tool()
async def send_checkin(slug: str, summary: str, details: str | None = None) -> str:
    """Send a checkin to a project's group chat."""
    return core.send(slug, messages.format_checkin(slug, summary, details))
```

**Registration:** Add to `.mcp.json` in consumer projects or globally:
```json
{
  "mcpServers": {
    "tool-telegram-whatsapp": {
      "command": "python",
      "args": ["-m", "whatsup.mcp_server"],
      "cwd": "/Users/.../tool-telegram-whatsapp"
    }
  }
}
```

### 4. Claude Skill (`/whatsup`)
**Consumer:** User via Claude Code conversation
**Why:** Skills are the UX layer — natural language shortcuts. Instead of remembering MCP tool names, the user types `/whatsup grassyknoll "Deployed v2"` and the skill translates to the right MCP call.

**Pattern:** A markdown file in `~/.claude/skills/` that instructs Claude on how to map user intent to MCP tools.

```markdown
When user says /whatsup:
- /whatsup <project> <message> → call send_checkin MCP tool
- /whatsup status → call whatsup_status MCP tool
- /whatsup projects → call whatsup_projects MCP tool
```

## The Core Layer

All four interfaces delegate to `core.py`, which contains the actual business logic:

```python
# whatsup/core.py

def send(slug: str, message: str) -> dict:
    """Send a message to a project's group."""
    cfg = config.get_project(slug)
    transport = _get_transport(cfg["transport"])
    return transport.send_message(cfg["groupId"], message)

def notify(slug: str, event: str, **data) -> dict:
    """Send a structured notification."""
    cfg = config.get_project(slug)
    if event not in cfg.get("notify", []):
        return {"skipped": True, "reason": f"event '{event}' not enabled for {slug}"}
    text = messages.format_event(event, slug=slug, **data)
    return send(slug, text)

def projects() -> list[dict]:
    """List all configured projects."""
    return config.get_all_projects()

def status() -> dict:
    """Health check all configured transports."""
    return {name: t.health_check() for name, t in _transports.items()}
```

## The Transport Protocol

```python
# whatsup/transport/__init__.py
from typing import Protocol

class Transport(Protocol):
    def send_message(self, group_id: str, text: str) -> dict: ...
    def create_group(self, name: str, members: list[str]) -> str: ...
    def health_check(self) -> dict: ...
```

Each transport implements this interface. Config selects which transport per project — you can have some projects on Telegram, others on WhatsApp.

## Key Design Decisions

1. **Core is sync, MCP is async** — core.py uses plain `requests` (sync). The MCP server wraps calls in `asyncio.to_thread()` if needed. Keeps the core simple.

2. **Config is file-based** — `~/.config/tool-telegram-whatsapp/config.json`. No database. Credentials + project mapping in one file.

3. **No shared state** — CLI, REST, and MCP all read the same config file and instantiate transports fresh. No daemon required for CLI usage.

4. **REST server is optional** — CLI and MCP work without the REST server running. The REST server is for external integrations that need HTTP.

5. **Message formatting is separate** — `messages.py` contains format functions. Transports send raw text. This means message templates work across both Telegram and WhatsApp.

## Afterburner Integration

The tool integrates with Afterburner via the CLI interface through the existing POST_MERGE_HOOKS system:

```bash
# In .sprint/config.sh
WHATSAPP_ENABLED="${WHATSAPP_ENABLED:-false}"

if [ "$WHATSAPP_ENABLED" = "true" ]; then
  POST_MERGE_HOOKS+=("whatsup notify ${PROJECT_SLUG} sprint-merged --sprint \${SPRINT_NUM} --status \${TEST_STATUS} --summary \"\${SPRINT_GOAL}\"")
fi
```

Sprint events → shell hook → CLI → core → transport → group chat. Clean separation.
