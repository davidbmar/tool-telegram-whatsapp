"""Telegram transport — sends messages via the Telegram Bot API."""

from __future__ import annotations

import requests

_API = "https://api.telegram.org/bot{token}"


class TelegramTransport:
    """Transport implementation backed by the Telegram Bot API.

    Parameters
    ----------
    bot_token:
        The bot token issued by @BotFather.
    """

    def __init__(self, bot_token: str) -> None:
        self._token = bot_token
        self._base = _API.format(token=bot_token)

    # ------------------------------------------------------------------
    # Transport protocol methods
    # ------------------------------------------------------------------

    def send_message(self, group_id: str, text: str) -> dict:
        """POST sendMessage to the Telegram Bot API."""
        try:
            resp = requests.post(
                f"{self._base}/sendMessage",
                json={"chat_id": group_id, "text": text},
                timeout=15,
            )
            return resp.json()
        except requests.RequestException as exc:
            return {"ok": False, "error": str(exc)}

    def create_group(self, name: str, members: list[str]) -> str:
        """Create an invite link for an existing group.

        The Telegram Bot API cannot create groups directly, so this
        creates an invite link for the group identified by *name*
        (which should be a chat_id).
        """
        try:
            resp = requests.post(
                f"{self._base}/createChatInviteLink",
                json={"chat_id": name},
                timeout=15,
            )
            data = resp.json()
            if data.get("ok"):
                return data["result"]["invite_link"]
            return data.get("description", "unknown error")
        except requests.RequestException as exc:
            return str(exc)

    def health_check(self) -> dict:
        """GET getMe — verifies the bot token is valid."""
        try:
            resp = requests.get(
                f"{self._base}/getMe",
                timeout=10,
            )
            data = resp.json()
            if data.get("ok"):
                return data["result"]
            return {"ok": False, "error": data.get("description", "unknown")}
        except requests.RequestException as exc:
            return {"ok": False, "error": str(exc)}
