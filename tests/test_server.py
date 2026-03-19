"""Tests for the whatsup REST server — schema & HTML view endpoints."""

import json
import threading
import time
import urllib.request

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


def _get_html(host, port, path):
    """Request a path with Accept: text/html and return the response body."""
    url = f"http://{host}:{port}{path}"
    req = urllib.request.Request(url, headers={"Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.headers.get("Content-Type").startswith("text/html")
        return resp.read().decode("utf-8")


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


class TestStatusEndpoint:
    def test_status_json_default(self, server):
        """No Accept header → JSON response."""
        host, port = server
        data = _get_json(host, port, "/status")
        assert "data" in data

    def test_status_html_view(self, server):
        """Accept: text/html → styled HTML page."""
        host, port = server
        html = _get_html(host, port, "/status")
        assert "Transport Status" in html
        assert "<nav" in html
        assert "var(--bg)" in html or "#0d1117" in html

    def test_status_html_has_nav_links(self, server):
        host, port = server
        html = _get_html(host, port, "/status")
        assert 'href="/config"' in html
        assert 'href="/projects"' in html
        assert 'href="/schema"' in html


class TestProjectsEndpoint:
    def test_projects_json_default(self, server):
        """No Accept header → JSON response."""
        host, port = server
        data = _get_json(host, port, "/projects")
        assert "data" in data

    def test_projects_html_view(self, server):
        """Accept: text/html → styled HTML table."""
        host, port = server
        html = _get_html(host, port, "/projects")
        assert "Projects" in html
        assert "<table" in html
        assert "<nav" in html

    def test_projects_html_has_config_link(self, server):
        host, port = server
        html = _get_html(host, port, "/projects")
        assert 'href="/config"' in html

    def test_projects_html_has_nav_links(self, server):
        host, port = server
        html = _get_html(host, port, "/projects")
        assert 'href="/"' in html
        assert 'href="/status"' in html
        assert 'href="/schema"' in html
