"""Tests for whatsup.messages — formatter functions and dispatch."""

import pytest
from whatsup.messages import (
    format_checkin,
    format_sprint_merged,
    format_test_failure,
    format_sprint_started,
    format_agent_completed,
    format_event,
)


def test_format_checkin_basic():
    result = format_checkin("my-proj", "all good")
    assert "Checkin" in result
    assert "my-proj" in result
    assert "all good" in result


def test_format_checkin_with_details():
    result = format_checkin("my-proj", "summary", details="extra info")
    assert "extra info" in result


def test_format_sprint_merged():
    result = format_sprint_merged("proj", sprint=3, branches=4, status="passed")
    assert "Sprint 3 merged" in result
    assert "4 branches" in result
    assert "passed" in result


def test_format_test_failure():
    result = format_test_failure("proj", sprint=2, agent="agentA", exit_code=1)
    assert "FAILED" in result
    assert "agentA" in result
    assert "Exit code: 1" in result


def test_format_sprint_started():
    result = format_sprint_started("proj", sprint=5, goal="ship it", agents="A,B", phases=2)
    assert "Sprint 5 started" in result
    assert "ship it" in result
    assert "Phases: 2" in result


def test_format_agent_completed():
    result = format_agent_completed("proj", sprint=1, agent="agentB", duration="5m", commits=3, remaining=1)
    assert "agentB" in result
    assert "3 commits" in result
    assert "1 agents remaining" in result


def test_format_event_dispatches_checkin():
    result = format_event("checkin", slug="demo", summary="hi")
    assert "Checkin" in result
    assert "demo" in result


def test_format_event_dispatches_sprint_merged():
    result = format_event("sprint-merged", slug="demo", sprint=1)
    assert "Sprint 1 merged" in result


def test_format_event_unknown_raises():
    with pytest.raises(ValueError, match="Unknown event 'bogus'"):
        format_event("bogus", slug="demo")
