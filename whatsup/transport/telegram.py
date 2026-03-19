"""Telegram transport implementation.

Stub — will be replaced by agentA-transport-config at merge time.
"""
from __future__ import annotations

import requests


class TelegramTransport:
    """Send messages via the Telegram Bot API."""

    def __init__(self, bot_token: str) -> None:
        self._token = bot_token
        self._base = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, group_id: str, text: str) -> dict:
        try:
            r = requests.post(
                f"{self._base}/sendMessage",
                json={"chat_id": group_id, "text": text},
                timeout=10,
            )
            return r.json()
        except requests.RequestException as exc:
            return {"ok": False, "error": str(exc)}

    def create_group(self, name: str, members: list[str]) -> str:
        try:
            r = requests.post(
                f"{self._base}/createChatInviteLink",
                json={"chat_id": name},
                timeout=10,
            )
            data = r.json()
            return data.get("result", {}).get("invite_link", "")
        except requests.RequestException as exc:
            return f"error: {exc}"

    def health_check(self) -> dict:
        try:
            r = requests.get(f"{self._base}/getMe", timeout=10)
            return r.json()
        except requests.RequestException as exc:
            return {"ok": False, "error": str(exc)}
