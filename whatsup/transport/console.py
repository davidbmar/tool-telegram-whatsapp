"""Console transport — prints messages to stdout instead of calling an API."""

from __future__ import annotations


class ConsoleTransport:
    """Transport that prints to stdout — useful for testing and demos."""

    def send_message(self, group_id: str, text: str) -> dict:
        """Print the message and return a success dict."""
        print(f"[console] → {group_id}: {text}")
        return {"ok": True, "transport": "console", "group_id": group_id}

    def create_group(self, name: str, members: list[str]) -> str:
        """Simulate group creation and return a fake ID."""
        print(f"[console] create_group({name!r}, {members!r})")
        return f"console-group-{name}"

    def health_check(self) -> dict:
        """Always healthy."""
        return {"ok": True, "transport": "console"}
