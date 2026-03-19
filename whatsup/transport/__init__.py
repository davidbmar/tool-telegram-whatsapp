"""Transport protocol definition.

Stub — will be replaced by agentA-transport-config at merge time.
"""
from __future__ import annotations

from typing import Protocol


class Transport(Protocol):
    def send_message(self, group_id: str, text: str) -> dict: ...
    def create_group(self, name: str, members: list[str]) -> str: ...
    def health_check(self) -> dict: ...
