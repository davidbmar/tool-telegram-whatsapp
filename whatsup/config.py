"""Configuration loader for tool-telegram-whatsapp.

Stub — will be replaced by agentA-transport-config at merge time.
"""
from __future__ import annotations

import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "tool-telegram-whatsapp" / "config.json"


def load_config() -> dict:
    """Read and return the config file."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Config file not found at {CONFIG_PATH}. "
            "Create it with your transport credentials and project definitions."
        )
    return json.loads(CONFIG_PATH.read_text())


def get_project(slug: str) -> dict:
    """Return project config by slug, or raise ValueError."""
    cfg = load_config()
    for proj in cfg.get("projects", []):
        if proj.get("slug") == slug:
            return proj
    raise ValueError(f"No project with slug '{slug}' found in config")


def get_all_projects() -> list[dict]:
    """Return all configured projects with their slugs."""
    cfg = load_config()
    return cfg.get("projects", [])
