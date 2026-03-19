<<<<<<< HEAD
"""Console transport — prints messages to stdout for testing and demos."""
=======
"""Console transport — prints messages to stdout instead of calling an API."""
>>>>>>> agentB-tests

from __future__ import annotations


class ConsoleTransport:
<<<<<<< HEAD
    """Transport that prints to stdout instead of calling an external API."""

    def send_message(self, group_id: str, text: str) -> dict:
        print(f"[whatsup → {group_id}] {text}")
        return {"ok": True, "transport": "console"}

    def create_group(self, name: str, members: list[str]) -> str:
        print(f"[whatsup] Creating console group '{name}' with members: {members}")
        return f"console-group-{name}"

    def health_check(self) -> dict:
        return {"ok": True, "transport": "console", "mode": "local"}
=======
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
>>>>>>> agentB-tests
