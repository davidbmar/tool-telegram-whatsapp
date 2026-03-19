"""Tests for the whatsup CLI — run as subprocess to test real entry point."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _run_cli(*args, config_path=None, history_dir=None, env_extra=None):
    """Run cli.py as a subprocess and return CompletedProcess."""
    cmd = [sys.executable, str(PROJECT_ROOT / "cli.py"), *args]
    env = None
    if env_extra:
        import os
        env = {**os.environ, **env_extra}
    return subprocess.run(cmd, capture_output=True, text=True, timeout=15, env=env)


@pytest.fixture()
def cli_env(tmp_path, monkeypatch):
    """Create a config for CLI subprocess tests and return env dict."""
    config = {
        "transports": {},
        "projects": [
            {
                "slug": "demo",
                "transport": "console",
                "groupId": "console-demo",
                "notify": ["checkin"],
            }
        ],
    }
    config_dir = tmp_path / ".config" / "tool-telegram-whatsapp"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    config_file.write_text(json.dumps(config), encoding="utf-8")

    history_dir = tmp_path / ".config" / "tool-telegram-whatsapp" / "history"
    history_dir.mkdir(parents=True)

    return {"HOME": str(tmp_path)}


def test_cli_help():
    result = _run_cli("--help")
    assert result.returncode == 0
    assert "whatsup" in result.stdout.lower() or "usage" in result.stdout.lower()


def test_cli_send(cli_env):
    result = _run_cli("send", "demo", "hello", env_extra=cli_env)
    assert result.returncode == 0
    assert "console" in result.stdout


def test_cli_projects(cli_env):
    result = _run_cli("projects", env_extra=cli_env)
    assert result.returncode == 0
    assert "demo" in result.stdout


def test_cli_status(cli_env):
    result = _run_cli("status", env_extra=cli_env)
    assert result.returncode == 0
    assert "console" in result.stdout


def test_cli_install_skill(tmp_path):
    """install-skill copies whatsup.md to ~/.claude/skills/."""
    fake_home = tmp_path / "fakehome"
    fake_home.mkdir()
    result = _run_cli("install-skill", env_extra={"HOME": str(fake_home)})
    assert result.returncode == 0
    assert "Skill installed" in result.stdout
    dest = fake_home / ".claude" / "skills" / "whatsup.md"
    assert dest.exists()
    assert dest.read_text(encoding="utf-8").strip() != ""
