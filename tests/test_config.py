"""Tests for whatsup.config — loading config and project lookup."""

import json
import pytest
from whatsup.config import load_config, get_project, get_all_projects


def test_load_config_reads_json(tmp_config):
    config = load_config()
    assert "projects" in config
    assert len(config["projects"]) == 1
    assert config["projects"][0]["slug"] == "demo"


def test_load_config_missing_raises(tmp_path, monkeypatch):
    missing = tmp_path / "does-not-exist.json"
    monkeypatch.setattr("whatsup.config.CONFIG_PATH", missing)
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        load_config()


def test_get_project_returns_correct(tmp_config):
    proj = get_project("demo")
    assert proj["slug"] == "demo"
    assert proj["transport"] == "console"


def test_get_project_unknown_raises(tmp_config):
    with pytest.raises(ValueError, match="not found"):
        get_project("nonexistent")


def test_get_all_projects_returns_list(tmp_config):
    projects = get_all_projects()
    assert isinstance(projects, list)
    assert len(projects) == 1
    assert projects[0]["slug"] == "demo"
