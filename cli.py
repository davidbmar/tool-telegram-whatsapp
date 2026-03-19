"""CLI entry point for whatsup — send messages to project group chats."""

import argparse
import json
import sys
from pathlib import Path

from whatsup import core
from whatsup import messages
from whatsup.config import CONFIG_PATH


def main():
    parser = argparse.ArgumentParser(
        prog="whatsup",
        description="Send messages and notifications to project group chats",
    )
    sub = parser.add_subparsers(dest="command")

    # send
    p_send = sub.add_parser("send", help="Send a checkin message")
    p_send.add_argument("slug", help="Project slug")
    p_send.add_argument("message", help="Checkin message text")

    # notify
    p_notify = sub.add_parser("notify", help="Send a lifecycle notification")
    p_notify.add_argument("slug", help="Project slug")
    p_notify.add_argument("event", help="Event type (sprint-merged, test-failure, …)")
    p_notify.add_argument("--sprint", type=int, default=None, help="Sprint number")
    p_notify.add_argument("--status", default=None, help="Test status (passed/failed)")
    p_notify.add_argument("--summary", default=None, help="Summary text")
    p_notify.add_argument("--agent", default=None, help="Agent name")
    p_notify.add_argument("--exit-code", type=int, default=None, help="Exit code")

    # projects
    sub.add_parser("projects", help="List configured projects")

    # status
    sub.add_parser("status", help="Check transport health")

    # init
    sub.add_parser("init", help="Create sample config for console transport")

    # install-skill
    sub.add_parser("install-skill", help="Install the whatsup Claude skill")

    # server
    p_server = sub.add_parser("server", help="Start the REST API server")
    p_server.add_argument("--port", type=int, default=None, help="Port (default: 1202)")

    # setup
    sub.add_parser("setup", help="First-time setup: init config, start server, open config UI")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "init":
            if CONFIG_PATH.exists():
                print(f"Config already exists at {CONFIG_PATH}")
                return
            sample = {
                "transports": {
                    "console": {},
                    "telegram": {"botToken": "YOUR_BOT_TOKEN_HERE"},
                },
                "projects": [
                    {
                        "slug": "demo",
                        "transport": "console",
                        "groupId": "demo-group",
                        "notify": [
                            "sprint-merged",
                            "test-failure",
                            "checkin",
                            "sprint-started",
                            "agent-completed",
                        ],
                    }
                ],
            }
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.write_text(json.dumps(sample, indent=2) + "\n", encoding="utf-8")
            print(f"Config created at {CONFIG_PATH}")
            print("Test with: whatsup send demo 'Hello world'")
            return

        elif args.command == "send":
            text = messages.format_checkin(args.slug, args.message)
            result = core.send(args.slug, text)
            print(json.dumps(result, indent=2))

        elif args.command == "notify":
            kwargs = {}
            if args.sprint is not None:
                kwargs["sprint"] = args.sprint
            if args.status is not None:
                kwargs["status"] = args.status
            if args.summary is not None:
                kwargs["summary"] = args.summary
            if args.agent is not None:
                kwargs["agent"] = args.agent
            if args.exit_code is not None:
                kwargs["exit_code"] = args.exit_code
            result = core.notify(args.slug, args.event, **kwargs)
            print(json.dumps(result, indent=2))

        elif args.command == "projects":
            projs = core.projects()
            if not projs:
                print("No projects configured.")
                return
            print(f"{'Slug':<20} {'Transport':<12} {'Group ID':<20}")
            print("-" * 52)
            for p in projs:
                print(f"{p.get('slug', ''):<20} {p.get('transport', ''):<12} {p.get('groupId', ''):<20}")

        elif args.command == "status":
            health = core.status()
            for transport_name, info in health.items():
                ok = info.get("ok", False)
                tag = "OK" if ok else "FAIL"
                print(f"{transport_name}: {tag}")
                if not ok and "error" in info:
                    print(f"  error: {info['error']}")

        elif args.command == "install-skill":
            skill_src = Path(__file__).resolve().parent / "skills" / "whatsup.md"
            if not skill_src.exists():
                print(f"Error: skill file not found at {skill_src}", file=sys.stderr)
                sys.exit(1)
            dest_dir = Path.home() / ".claude" / "skills"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / "whatsup.md"
            import shutil
            shutil.copy2(skill_src, dest)
            print(f"Skill installed to {dest}")

        elif args.command == "server":
            from whatsup.server import main as server_main
            argv = []
            if args.port is not None:
                argv.extend(["--port", str(args.port)])
            server_main(argv)

        elif args.command == "setup":
            import subprocess, os, time, webbrowser
            # Step 1: Init config if needed
            if not CONFIG_PATH.exists():
                print("Step 1/3: Creating config...")
                sample = {
                    "transports": {"console": {}, "telegram": {"botToken": ""}},
                    "projects": [{"slug": "demo", "transport": "console",
                        "groupId": "demo-group",
                        "notify": ["sprint-merged", "test-failure", "checkin",
                                   "sprint-started", "agent-completed"]}],
                }
                CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
                CONFIG_PATH.write_text(json.dumps(sample, indent=2) + "\n", encoding="utf-8")
                print(f"  Config created at {CONFIG_PATH}")
            else:
                print("Step 1/3: Config exists.")

            # Step 2: Start server in background
            print("Step 2/3: Starting server...")
            port = 1202
            # Kill stale server
            try:
                pids = subprocess.check_output(["lsof", "-ti", f":{port}"], text=True).strip()
                for pid in pids.splitlines():
                    pid = int(pid)
                    if pid != os.getpid():
                        os.kill(pid, 15)
            except (subprocess.CalledProcessError, OSError):
                pass
            time.sleep(0.5)
            # Launch in background
            log_path = Path.home() / ".config" / "tool-telegram-whatsapp" / "server.log"
            pid_path = Path.home() / ".config" / "tool-telegram-whatsapp" / "server.pid"
            server_script = Path(__file__).resolve().parent / "whatsup" / "server.py"
            proc = subprocess.Popen(
                [sys.executable, "-m", "whatsup.server", "--port", str(port)],
                stdout=open(log_path, "w"), stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            pid_path.write_text(str(proc.pid))
            time.sleep(1)
            print(f"  Server running on http://localhost:{port} (PID {proc.pid})")
            print(f"  Log: {log_path}")

            # Step 3: Open config UI
            print("Step 3/3: Opening config UI...")
            url = f"http://localhost:{port}/config"
            webbrowser.open(url)
            print(f"\n  Config UI: {url}")
            print(f"\n  To connect Telegram:")
            print(f"  1. Message @BotFather on Telegram -> /newbot -> get token")
            print(f"  2. Paste the token in the Telegram Bot Token field")
            print(f"  3. Create a Telegram group, add the bot")
            print(f"  4. Get group ID: curl https://api.telegram.org/bot<TOKEN>/getUpdates")
            print(f"  5. Set transport to 'telegram', paste group ID, click Save")
            print(f"  6. Click 'Send Test Message' to verify")

    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
