"""Tests for whatsup.core — send, notify, projects, status."""

import pytest
from whatsup import core


def test_send_console_transport(tmp_config, clean_history, capsys):
    result = core.send("demo", "hello world")
    assert result["ok"] is True
    assert result["transport"] == "console"
    captured = capsys.readouterr()
    assert "hello world" in captured.out


def test_notify_event_in_list(tmp_config, clean_history, capsys):
    result = core.notify("demo", "checkin", summary="all good")
    assert result["ok"] is True
    captured = capsys.readouterr()
    assert "Checkin" in captured.out


def test_notify_event_not_in_list(tmp_config, clean_history):
    result = core.notify("demo", "agent-completed", sprint=1, agent="X", duration="1m", commits=1, remaining=0)
    assert result["skipped"] is True
    assert "not in notify list" in result["reason"]


def test_projects_returns_list(tmp_config):
    projs = core.projects()
    assert isinstance(projs, list)
    assert len(projs) == 1
    assert projs[0]["slug"] == "demo"


def test_status_returns_health_dict(tmp_config):
    health = core.status()
    assert "console" in health
    assert health["console"]["ok"] is True
