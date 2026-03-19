"""MCP server exposing whatsup tools for Claude Code integration."""

import json
import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    FastMCP = None

from whatsup import core
from whatsup import messages


def _mcp_not_installed():
    print(
        "MCP package not installed. Install with: pip install mcp",
        file=sys.stderr,
    )
    sys.exit(1)


if FastMCP is None:
    # Create a minimal stub so the module can still be imported,
    # but running the server will print a helpful error and exit.
    class _StubMCP:
        def __init__(self, *a, **kw): pass
        def tool(self):
            def _dec(fn): return fn
            return _dec
        def run(self, **kw): _mcp_not_installed()

    mcp = _StubMCP()
else:
    mcp = FastMCP("tool-telegram-whatsapp")


@mcp.tool()
def send_checkin(slug: str, summary: str, details: str | None = None) -> str:
    """Send a checkin to a project's group chat."""
    text = messages.format_checkin(slug, summary, details)
    result = core.send(slug, text)
    return json.dumps(result)


@mcp.tool()
def send_notification(
    slug: str,
    event: str,
    sprint: int | None = None,
    status: str | None = None,
    summary: str | None = None,
) -> str:
    """Send a sprint lifecycle notification."""
    kwargs = {}
    if sprint is not None:
        kwargs["sprint"] = sprint
    if status is not None:
        kwargs["status"] = status
    if summary is not None:
        kwargs["summary"] = summary
    result = core.notify(slug, event, **kwargs)
    return json.dumps(result)


@mcp.tool()
def whatsup_projects() -> str:
    """List projects with messaging configured."""
    return json.dumps(core.projects())


@mcp.tool()
def whatsup_status() -> str:
    """Check transport connection status."""
    return json.dumps(core.status())


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
