"""JSONL message history logging per project."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

HISTORY_DIR = Path.home() / ".config" / "tool-telegram-whatsapp" / "history"


def log_message(
    slug: str,
    direction: str,
    event: str,
    message: str,
    result: dict,
) -> None:
    """Append a JSON line to the project's history file."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "direction": direction,
        "event": event,
        "message": message,
        "result": result,
    }
    path = HISTORY_DIR / f"{slug}.jsonl"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def get_history(slug: str, limit: int = 20) -> list[dict]:
    """Read the last *limit* entries from a project's history file."""
    path = HISTORY_DIR / f"{slug}.jsonl"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    recent = lines[-limit:] if limit else lines
    return [json.loads(line) for line in recent]
