"""Shared fixtures for whatsup tests."""

import json
import pytest
from pathlib import Path


@pytest.fixture()
def tmp_config(tmp_path, monkeypatch):
    """Create a temporary config.json with console transport and a demo project."""
    config = {
        "transports": {},
        "projects": [
            {
                "slug": "demo",
                "transport": "console",
                "groupId": "console-demo",
                "notify": ["checkin", "sprint-merged", "test-failure"],
            }
        ],
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config), encoding="utf-8")
    monkeypatch.setattr("whatsup.config.CONFIG_PATH", config_file)
    return config_file


@pytest.fixture()
def clean_history(tmp_path, monkeypatch):
    """Point history storage at a temporary directory."""
    history_dir = tmp_path / "history"
    history_dir.mkdir()
    monkeypatch.setattr("whatsup.history.HISTORY_DIR", history_dir)
    return history_dir
