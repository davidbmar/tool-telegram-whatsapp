"""Tests for the whatsup REST server — schema endpoint and config token auth."""

import json
import os
import threading
import time
import urllib.request
import urllib.error

import pytest

from whatsup.server import _ThreadedHTTPServer, WhatsupHandler


@pytest.fixture()
def server():
    """Start the server on an ephemeral port and yield (host, port)."""
    httpd = _ThreadedHTTPServer(("127.0.0.1", 0), WhatsupHandler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    yield ("127.0.0.1", port)
    httpd.shutdown()
    httpd.server_close()


def _get_json(host, port, path):
    url = f"http://{host}:{port}{path}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read())


class TestSchemaEndpoint:
    def test_schema_returns_valid_json(self, server):
        host, port = server
        data = _get_json(host, port, "/schema")
        assert "tool" in data
        assert "globalConfig" in data
        assert "projectConfig" in data

    def test_schema_tool_name(self, server):
        host, port = server
        data = _get_json(host, port, "/schema")
        assert data["tool"] == "tool-telegram-whatsapp"

    def test_schema_version(self, server):
        host, port = server
        data = _get_json(host, port, "/schema")
        assert data["version"] == "0.1.0"

    def test_schema_project_config_properties(self, server):
        host, port = server
        data = _get_json(host, port, "/schema")
        props = data["projectConfig"]["properties"]
        assert "transport" in props
        assert "groupId" in props
        assert "notify" in props

    def test_schema_transport_enum(self, server):
        host, port = server
        data = _get_json(host, port, "/schema")
        transport = data["projectConfig"]["properties"]["transport"]
        assert set(transport["enum"]) == {"telegram", "console", "whatsapp"}

    def test_schema_groupid_required(self, server):
        host, port = server
        data = _get_json(host, port, "/schema")
        assert "groupId" in data["projectConfig"]["required"]

    def test_schema_global_config_telegram(self, server):
        host, port = server
        data = _get_json(host, port, "/schema")
        telegram = data["globalConfig"]["properties"]["telegram"]
        assert telegram["properties"]["botToken"]["sensitive"] is True


def _post_json(host, port, path, data, headers=None):
    """POST JSON and return (status_code, response_dict)."""
    url = f"http://{host}:{port}{path}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


class TestConfigTokenAuth:
    """Token-based protection for POST /api/config."""

    def test_no_token_env_allows_post(self, server, tmp_config, monkeypatch):
        """When WHATSUP_API_TOKEN is unset, POST should succeed."""
        monkeypatch.delenv("WHATSUP_API_TOKEN", raising=False)
        host, port = server
        payload = {"transports": {"console": {}}, "projects": []}
        status, data = _post_json(host, port, "/api/config", payload)
        assert status == 200
        assert data["ok"] is True

    def test_token_env_rejects_missing_token(self, server, tmp_config, monkeypatch):
        """When WHATSUP_API_TOKEN is set, POST without token returns 403."""
        monkeypatch.setenv("WHATSUP_API_TOKEN", "s3cret")
        host, port = server
        payload = {"transports": {"console": {}}, "projects": []}
        status, data = _post_json(host, port, "/api/config", payload)
        assert status == 403
        assert data["ok"] is False

    def test_token_env_rejects_wrong_token(self, server, tmp_config, monkeypatch):
        """Wrong token in header returns 403."""
        monkeypatch.setenv("WHATSUP_API_TOKEN", "s3cret")
        host, port = server
        payload = {"transports": {"console": {}}, "projects": []}
        status, data = _post_json(host, port, "/api/config", payload,
                                  headers={"X-Whatsup-Token": "wrong"})
        assert status == 403
        assert data["ok"] is False

    def test_token_via_header(self, server, tmp_config, monkeypatch):
        """Correct token in X-Whatsup-Token header allows POST."""
        monkeypatch.setenv("WHATSUP_API_TOKEN", "s3cret")
        host, port = server
        payload = {"transports": {"console": {}}, "projects": []}
        status, data = _post_json(host, port, "/api/config", payload,
                                  headers={"X-Whatsup-Token": "s3cret"})
        assert status == 200
        assert data["ok"] is True

    def test_token_via_query_param(self, server, tmp_config, monkeypatch):
        """Correct token in query parameter allows POST."""
        monkeypatch.setenv("WHATSUP_API_TOKEN", "s3cret")
        host, port = server
        payload = {"transports": {"console": {}}, "projects": []}
        status, data = _post_json(host, port, "/api/config?token=s3cret", payload)
        assert status == 200
        assert data["ok"] is True
