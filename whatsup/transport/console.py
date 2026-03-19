"""Console transport — prints messages to stdout for testing and demos."""

from __future__ import annotations


class ConsoleTransport:
    """Transport that prints to stdout instead of calling an external API."""

    def send_message(self, group_id: str, text: str) -> dict:
        print(f"[whatsup → {group_id}] {text}")
        return {"ok": True, "transport": "console", "group_id": group_id}

    def create_group(self, name: str, members: list[str]) -> str:
        print(f"[whatsup] Creating console group '{name}' with members: {members}")
        return f"console-group-{name}"

    def health_check(self) -> dict:
        return {"ok": True, "transport": "console", "mode": "local"}
