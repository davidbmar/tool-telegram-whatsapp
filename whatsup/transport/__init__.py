"""Pluggable transport layer — defines the Transport protocol."""

from __future__ import annotations

from typing import Protocol


class Transport(Protocol):
    """Interface every messaging transport must implement."""

    def send_message(self, group_id: str, text: str) -> dict: ...

    def create_group(self, name: str, members: list[str]) -> str: ...

    def health_check(self) -> dict: ...


__all__ = ["Transport"]
