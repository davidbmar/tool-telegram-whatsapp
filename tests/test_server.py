"""Tests for the whatsup REST server — schema endpoint."""

import json
import threading
import time
import urllib.request

import pytest

from whatsup.server import _ThreadedHTTPServer, _Handler


@pytest.fixture()
def server():
    """Start the server on an ephemeral port and yield (host, port)."""
    httpd = _ThreadedHTTPServer(("127.0.0.1", 0), _Handler)
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
