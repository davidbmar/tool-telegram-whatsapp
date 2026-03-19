"""Core business logic — send, notify, projects, status."""
from __future__ import annotations

from whatsup import config, messages
from whatsup.transport import Transport
from whatsup.transport.telegram import TelegramTransport


def _get_transport(transport_name: str, transport_config: dict) -> Transport:
    """Instantiate the right transport based on name."""
    if transport_name == "telegram":
        return TelegramTransport(bot_token=transport_config["bot_token"])
    raise ValueError(f"Unknown transport '{transport_name}'")


def send(slug: str, message: str) -> dict:
    """Load config, resolve transport, and send a message."""
    proj = config.get_project(slug)
    cfg = config.load_config()
    transport_name = proj["transport"]
    transport_cfg = cfg.get("transports", {}).get(transport_name, {})
    transport = _get_transport(transport_name, transport_cfg)
    return transport.send_message(proj["groupId"], message)


def notify(slug: str, event: str, **data) -> dict:
    """Send a notification if the event is enabled for the project."""
    proj = config.get_project(slug)
    notify_list = proj.get("notify", [])
    if event not in notify_list:
        return {"skipped": True, "reason": f"Event '{event}' not in notify list for '{slug}'"}
    msg = messages.format_event(event, slug=slug, **data)
    return send(slug, msg)


def projects() -> list[dict]:
    """Return all configured projects."""
    return config.get_all_projects()


def status() -> dict:
    """Health-check each unique transport, return transport_name → result."""
    cfg = config.load_config()
    transports_cfg = cfg.get("transports", {})
    results = {}
    for name, tcfg in transports_cfg.items():
        try:
            transport = _get_transport(name, tcfg)
            results[name] = transport.health_check()
        except ValueError:
            results[name] = {"ok": False, "error": f"Unknown transport '{name}'"}
    return results
