"""Tests for whatsup.history — JSONL logging and retrieval."""

from whatsup.history import log_message, get_history


def test_log_message_creates_file(clean_history):
    log_message("demo", "outbound", "send", "hello", {"ok": True})
    path = clean_history / "demo.jsonl"
    assert path.exists()
    lines = path.read_text().strip().splitlines()
    assert len(lines) == 1


def test_log_message_appends(clean_history):
    log_message("demo", "outbound", "send", "first", {"ok": True})
    log_message("demo", "outbound", "send", "second", {"ok": True})
    path = clean_history / "demo.jsonl"
    lines = path.read_text().strip().splitlines()
    assert len(lines) == 2


def test_get_history_reads_back(clean_history):
    log_message("demo", "outbound", "send", "msg1", {"ok": True})
    log_message("demo", "outbound", "send", "msg2", {"ok": True})
    history = get_history("demo")
    assert len(history) == 2
    assert history[0]["message"] == "msg1"
    assert history[1]["message"] == "msg2"


def test_get_history_with_limit(clean_history):
    for i in range(10):
        log_message("demo", "outbound", "send", f"msg{i}", {"ok": True})
    history = get_history("demo", limit=3)
    assert len(history) == 3
    assert history[0]["message"] == "msg7"
