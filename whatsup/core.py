"""Core business logic for the whatsup package."""

from __future__ import annotations

# Backward-compatible re-exports — keep so `from whatsup import core`
# then `core.load_config` etc. still works.
from whatsup.config import get_all_projects, get_project, load_config  # noqa: F401
from whatsup.transport import Transport  # noqa: F401
from whatsup.transport.telegram import TelegramTransport  # noqa: F401

from whatsup import messages
from whatsup.config import get_all_projects as _get_all_projects
from whatsup.config import get_project as _get_project
from whatsup.config import load_config as _load_config
from whatsup.history import log_message


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _get_transport(transport_name: str, transports_config: dict) -> TelegramTransport:
    """Return a transport instance based on *transport_name*."""
    if transport_name == "telegram":
        token = transports_config.get("telegram", {}).get("botToken", "")
        return TelegramTransport(bot_token=token)
    raise ValueError(f"Unknown transport: {transport_name}")


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

def send(slug: str, message: str) -> dict:
    """Send *message* to the project's group chat and log it."""
    config = _load_config()
    project = _get_project(slug)
    transport_name = project.get("transport", "telegram")
    transport = _get_transport(transport_name, config.get("transports", {}))
    group_id = project.get("groupId", "")
    result = transport.send_message(group_id, message)
    log_message(slug, "outbound", "send", message, result)
    return result


def notify(slug: str, event: str, **data) -> dict:
    """Send a notification if the event is in the project's notify list."""
    project = _get_project(slug)
    notify_list = project.get("notify", [])
    if event not in notify_list:
        return {"skipped": True, "reason": f"Event '{event}' not in notify list for '{slug}'"}
    message = messages.format_event(event, slug=slug, **data)
    return send(slug, message)


def projects() -> list[dict]:
    """Return all configured projects with slugs."""
    return _get_all_projects()


def status() -> dict:
    """Health-check each unique transport."""
    config = _load_config()
    transports_config = config.get("transports", {})
    all_projects = _get_all_projects()

    # Collect unique transport names
    transport_names = {p.get("transport", "telegram") for p in all_projects}

    results = {}
    for name in sorted(transport_names):
        try:
            t = _get_transport(name, transports_config)
            results[name] = t.health_check()
        except Exception as exc:
            results[name] = {"ok": False, "error": str(exc)}
    return results
