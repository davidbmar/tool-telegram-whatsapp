"""MCP server exposing whatsup tools for Claude Code integration."""

import json

from mcp.server.fastmcp import FastMCP

from whatsup import core
from whatsup import messages

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
