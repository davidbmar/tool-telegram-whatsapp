"""Core business logic — send, notify, projects, status.

Stub — full implementation provided by agentB-core-messages branch.
"""

from whatsup import messages


def _load_config():
    from whatsup.config import load_config
    return load_config()


def _get_transport(transport_name: str, config: dict):
    if transport_name == "telegram":
        from whatsup.transport.telegram import TelegramTransport
        token = config.get("transports", {}).get("telegram", {}).get("botToken", "")
        return TelegramTransport(token)
    raise ValueError(f"Unknown transport: {transport_name}")


def send(slug: str, message: str) -> dict:
    from whatsup.config import get_project
    cfg = _load_config()
    proj = get_project(slug)
    transport = _get_transport(proj["transport"], cfg)
    return transport.send_message(proj["groupId"], message)


def notify(slug: str, event: str, **data) -> dict:
    from whatsup.config import get_project
    proj = get_project(slug)
    notify_list = proj.get("notify", [])
    if event not in notify_list:
        return {"skipped": True, "reason": f"Event '{event}' not enabled for project '{slug}'"}
    text = messages.format_event(event, slug=slug, **data)
    cfg = _load_config()
    transport = _get_transport(proj["transport"], cfg)
    return transport.send_message(proj["groupId"], text)


def projects() -> list[dict]:
    from whatsup.config import get_all_projects
    return get_all_projects()


def status() -> dict:
    cfg = _load_config()
    results = {}
    transports_cfg = cfg.get("transports", {})
    for name, tcfg in transports_cfg.items():
        try:
            transport = _get_transport(name, cfg)
            results[name] = transport.health_check()
        except Exception as exc:
            results[name] = {"ok": False, "error": str(exc)}
    return results
