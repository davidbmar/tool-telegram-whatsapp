"""REST API server for whatsup — HTTP interface on port 1202."""

from __future__ import annotations

import argparse
import json
import logging
import os
import signal
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

from whatsup import core

log = logging.getLogger("whatsup.server")

DEFAULT_PORT = 1202
_CONFIG_PAGE_PATH = os.path.join(os.path.dirname(__file__), "config_ui.html")


# ------------------------------------------------------------------
# Threaded HTTP server (matches Afterburner dashboard pattern)
# ------------------------------------------------------------------

class _ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


# ------------------------------------------------------------------
# Request handler
# ------------------------------------------------------------------

class WhatsupHandler(BaseHTTPRequestHandler):

    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict | None:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return None

    def _send_html(self, html: str, status: int = 200) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # --- GET routes -------------------------------------------------

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/projects":
            self._handle_projects()
        elif path == "/status":
            self._handle_status()
        elif path == "/history":
            params = parse_qs(parsed.query)
            self._handle_history(params)
        elif path == "/schema":
            self._handle_schema()
        elif path == "/config":
            self._handle_config_page()
        elif path == "/api/config":
            self._handle_config_get()
        elif path == "":
            self._handle_index()
        else:
            self._send_json({"ok": False, "error": "Not found"}, 404)

    # --- POST routes ------------------------------------------------

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        body = self._read_json()
        if body is None:
            self._send_json({"ok": False, "error": "Invalid or missing JSON body"}, 400)
            return

        if path == "/send":
            self._handle_send(body)
        elif path == "/notify":
            self._handle_notify(body)
        elif path == "/api/config":
            self._handle_config_save(body)
        else:
            self._send_json({"ok": False, "error": "Not found"}, 404)

    # --- Endpoint implementations -----------------------------------

    def _handle_send(self, body: dict) -> None:
        slug = body.get("slug")
        message = body.get("message")
        if not slug or not message:
            self._send_json({"ok": False, "error": "Missing 'slug' or 'message'"}, 400)
            return
        try:
            result = core.send(slug, message)
            self._send_json({"ok": True, "data": result})
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, 500)

    def _handle_notify(self, body: dict) -> None:
        slug = body.get("slug")
        event = body.get("event")
        if not slug or not event:
            self._send_json({"ok": False, "error": "Missing 'slug' or 'event'"}, 400)
            return
        kwargs = {}
        for key in ("sprint", "status", "summary", "agent", "exit_code"):
            if key in body:
                kwargs[key] = body[key]
        try:
            result = core.notify(slug, event, **kwargs)
            self._send_json({"ok": True, "data": result})
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, 500)

    def _handle_projects(self) -> None:
        try:
            result = core.projects()
            self._send_json({"ok": True, "data": result})
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, 500)

    def _handle_status(self) -> None:
        try:
            result = core.status()
            self._send_json({"ok": True, "data": result})
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, 500)

    def _handle_schema(self) -> None:
        from whatsup import __version__
        schema = {
            "tool": "tool-telegram-whatsapp",
            "version": __version__,
            "description": "Per-project group-chat messaging via Telegram/WhatsApp",
            "globalConfig": {
                "type": "object",
                "properties": {
                    "telegram": {
                        "type": "object",
                        "properties": {
                            "botToken": {
                                "type": "string",
                                "description": "Telegram Bot API token",
                                "sensitive": True,
                            }
                        },
                    },
                    "console": {"type": "object", "properties": {}},
                },
            },
            "projectConfig": {
                "type": "object",
                "properties": {
                    "transport": {
                        "type": "string",
                        "enum": ["telegram", "console", "whatsapp"],
                        "default": "console",
                    },
                    "groupId": {
                        "type": "string",
                        "description": "Chat group ID",
                    },
                    "notify": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "sprint-started",
                                "agent-completed",
                                "sprint-merged",
                                "test-failure",
                                "checkin",
                            ],
                        },
                        "default": ["sprint-merged", "test-failure"],
                    },
                },
                "required": ["groupId"],
            },
        }
        self._send_json(schema)

    def _handle_index(self) -> None:
        self._send_html("""<!DOCTYPE html><html><head><meta charset="utf-8">
        <title>whatsup</title>
        <style>body{font-family:system-ui;max-width:600px;margin:40px auto;padding:0 20px;background:#0d1117;color:#e6edf3}
        a{color:#58a6ff}h1{margin-bottom:4px}.sub{color:#8b949e;margin-bottom:24px}
        .card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:20px;margin-bottom:16px}
        .card h2{color:#58a6ff;font-size:16px;margin-bottom:8px}.card p{color:#8b949e;font-size:14px}
        .btn{display:inline-block;padding:10px 20px;background:#58a6ff;color:#fff;text-decoration:none;border-radius:6px;font-weight:600;margin-top:8px}</style>
        </head><body>
        <h1>whatsup</h1>
        <p class="sub">Per-project group-chat messaging for Afterburner sprints</p>
        <div class="card"><h2>Get Started</h2>
        <p>New here? Set up Telegram messaging in 5 minutes.</p>
        <a href="/config" class="btn">Open Setup Guide &rarr;</a></div>
        <div class="card"><h2>Quick Links</h2>
        <p><a href="/config">Configuration UI</a> &mdash; manage transports, projects, and events</p>
        <p><a href="/status">Transport Status</a> &mdash; check if transports are healthy</p>
        <p><a href="/projects">Projects</a> &mdash; list configured projects (JSON)</p>
        <p><a href="/schema">Config Schema</a> &mdash; JSON Schema for plugin integration</p>
        </div></body></html>""")

    def _handle_config_get(self) -> None:
        try:
            from whatsup.config import CONFIG_PATH
            if CONFIG_PATH.exists():
                config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
                # Mask sensitive fields
                for t_name, t_cfg in config.get("transports", {}).items():
                    if "botToken" in t_cfg and len(t_cfg["botToken"]) > 10:
                        t_cfg["botToken"] = t_cfg["botToken"][:8] + "..."
                    if "accessToken" in t_cfg and len(t_cfg["accessToken"]) > 10:
                        t_cfg["accessToken"] = t_cfg["accessToken"][:8] + "..."
                self._send_json({"ok": True, "data": config, "path": str(CONFIG_PATH)})
            else:
                self._send_json({"ok": False, "error": "No config file", "path": str(CONFIG_PATH)})
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, 500)

    def _check_config_token(self) -> bool:
        """Return True if the request carries a valid token (or no token is required)."""
        expected = os.environ.get("WHATSUP_API_TOKEN", "")
        if not expected:
            return True  # no token configured — allow all
        token = self.headers.get("X-Whatsup-Token", "")
        if not token:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            token = (params.get("token") or [""])[0]
        return token == expected

    def _handle_config_save(self, body: dict) -> None:
        if not self._check_config_token():
            self._send_json({"ok": False, "error": "Forbidden — invalid or missing token"}, 403)
            return
        try:
            from whatsup.config import CONFIG_PATH
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            # Merge: if existing config has full tokens, preserve them when masked
            if CONFIG_PATH.exists():
                existing = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
                for t_name, t_cfg in body.get("transports", {}).items():
                    if "botToken" in t_cfg and t_cfg["botToken"].endswith("..."):
                        old_token = existing.get("transports", {}).get(t_name, {}).get("botToken", "")
                        t_cfg["botToken"] = old_token
                    if "accessToken" in t_cfg and t_cfg["accessToken"].endswith("..."):
                        old_token = existing.get("transports", {}).get(t_name, {}).get("accessToken", "")
                        t_cfg["accessToken"] = old_token
            CONFIG_PATH.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
            self._send_json({"ok": True, "message": "Config saved"})
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, 500)

    def _handle_config_page(self) -> None:
        try:
            with open(_CONFIG_PAGE_PATH, encoding="utf-8") as f:
                self._send_html(f.read())
        except FileNotFoundError:
            self._send_html("<h1>Config UI not found</h1><p>Missing config_ui.html</p>", 500)

    def _handle_history(self, params: dict) -> None:
        slug_list = params.get("slug", [])
        if not slug_list:
            self._send_json({"ok": False, "error": "Missing 'slug' query parameter"}, 400)
            return
        slug = slug_list[0]
        limit = 20
        limit_list = params.get("limit", [])
        if limit_list:
            try:
                limit = int(limit_list[0])
            except ValueError:
                pass
        try:
            from whatsup import history  # lazy import — module added by agentB
            result = history.get_history(slug, limit=limit)
            self._send_json({"ok": True, "data": result})
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, 500)

    # suppress default stderr logging per request
    def log_message(self, fmt, *args) -> None:
        log.info(fmt, *args)


# ------------------------------------------------------------------
# Stale process cleanup
# ------------------------------------------------------------------

def _kill_stale_server(port: int) -> None:
    try:
        pids = subprocess.check_output(
            ["lsof", "-ti", f":{port}"], text=True,
        ).strip()
        for pid_str in pids.splitlines():
            pid = int(pid_str)
            if pid != os.getpid():
                os.kill(pid, signal.SIGTERM)
                log.info("Killed stale process %d on port %d", pid, port)
    except (subprocess.CalledProcessError, OSError):
        pass


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="whatsup-server",
        description="REST API server for whatsup notifications (port 1202)",
    )
    parser.add_argument(
        "--port", type=int,
        default=int(os.environ.get("WHATSUP_PORT", DEFAULT_PORT)),
        help=f"Port to listen on (default: {DEFAULT_PORT}, env: WHATSUP_PORT)",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(message)s",
    )

    port = args.port
    _kill_stale_server(port)

    bind_addr = os.environ.get("WHATSUP_BIND", "127.0.0.1")
    server = _ThreadedHTTPServer((bind_addr, port), WhatsupHandler)

    # Graceful shutdown on SIGINT / SIGTERM
    def _shutdown(signum, _frame):
        log.info("Received signal %d — shutting down", signum)
        server.shutdown()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    log.info("whatsup REST server starting on %s:%d", bind_addr, port)
    try:
        server.serve_forever()
    finally:
        server.server_close()
        log.info("Server stopped.")


if __name__ == "__main__":
    main()
