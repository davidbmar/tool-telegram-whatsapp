"""Configuration loader for tool-telegram-whatsapp.

Reads ~/.config/tool-telegram-whatsapp/config.json and exposes
project-level settings (transport type, group ID, notify list).
"""

from __future__ import annotations

import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "tool-telegram-whatsapp" / "config.json"


def load_config() -> dict:
    """Read and parse the JSON config file.

    Raises FileNotFoundError with a helpful message when the file is missing.
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Config file not found at {CONFIG_PATH}. "
            "Create it with at least: "
            '{"projects": [{"slug": "my-project", "transport": "telegram", '
            '"groupId": "...", "notify": []}]}'
        )
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def get_project(slug: str) -> dict:
    """Return the project config for *slug*.

    Raises ValueError if the slug is not found.
    """
    config = load_config()
    for project in config.get("projects", []):
        if project.get("slug") == slug:
            return project
    raise ValueError(
        f"Project '{slug}' not found in config. "
        f"Available: {[p.get('slug') for p in config.get('projects', [])]}"
    )


def get_all_projects() -> list[dict]:
    """Return every configured project with its slug."""
    config = load_config()
    return config.get("projects", [])
