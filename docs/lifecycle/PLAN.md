# Plan

## Problem
Afterburner's sprint pipeline runs autonomously but has no way to push status updates to developers' phones. The dashboard is pull-based (you watch it), but sprints can run 30-60 minutes. We need a push-based notification tool that sends sprint events and manual checkins to per-project group chats on Telegram (now) and WhatsApp (later).

## Appetite
**Small batch — 1 sprint for Phase 1.** The core package is ~400 lines of Python across 8 files. Telegram transport is trivially simple (one HTTP POST per message). The complexity budget is intentionally low: no database, no daemon, no frontend. File-based config, `requests` library, done.

## Solution Sketch
A Python package called `whatsup` with a pluggable transport layer. Four interfaces (CLI, REST, MCP, Claude skill) all delegate to a single `core.py`. Each Afterburner project maps to a messaging group via `~/.config/tool-telegram-whatsapp/config.json`. Sprint lifecycle events trigger notifications through Afterburner's existing POST_MERGE_HOOKS system, which shells out to the `whatsup` CLI.

The transport protocol is a 3-method Python Protocol class (`send_message`, `create_group`, `health_check`). Telegram implements it first. WhatsApp implements it in Phase 3 when Meta Business verification is approved. Projects can independently choose their transport.

## Market Fit Analysis
This fills a gap specific to the Afterburner ecosystem. No existing tool provides sprint-aware notifications with per-project scoping across multiple transports. The closest alternatives are generic webhook tools (lack sprint context), OpenClaw/NanoClaw (heavy — full AI agent frameworks), or manual "check the dashboard" workflows (what we're replacing). The tool is purpose-built for a known user with a known workflow.

## Differentiation Strategy
The moat is Afterburner integration depth — this tool understands sprint lifecycle events, project slugs, and POST_MERGE_HOOKS natively. It's not a generic messaging wrapper. The multi-interface approach (CLI + REST + MCP + skill) means it's usable from every context: shell scripts, services, AI agents, and conversation.

## Rabbit Holes
- **WhatsApp Business verification:** Getting Official Business Account (green tick) for the Groups API is hard for solo devs. Don't block on this — Telegram first.
- **Inbound message handling:** Receiving and responding to messages in groups adds major complexity (webhook servers, NLP, agent loops). Defer entirely — this is outbound-only for Phase 1-2.
- **Message history search:** Storing and indexing all messages for full-text search. Nice to have but not MVP. A simple JSONL append log is sufficient.
- **Rich message formatting:** Telegram supports markdown, WhatsApp has templates with variables. Don't over-invest in formatting parity across transports — plain text works everywhere.

## No-Gos
- No AI agent in the group chat (that's NanoClaw/OpenClaw territory)
- No inbound message processing in Phase 1-2
- No web UI or dashboard (use Afterburner's dashboard for that)
- No database — file-based config and JSONL history only
- No multi-tenancy — single user, single bot token per transport
- No SMS, email, Slack, or Discord transports (unless demand emerges)

## Sprint Candidates

### Sprint 1: Core + Telegram + CLI + MCP
- Create repo with pyproject.toml and entry point
- `config.py` — load `~/.config/tool-telegram-whatsapp/config.json`
- `transport/__init__.py` — Transport protocol
- `transport/telegram.py` — Telegram Bot API client
- `messages.py` — format_checkin, format_sprint_merged, format_test_failure
- `core.py` — send, notify, projects, status
- `cli.py` — argparse: send, notify, projects, status subcommands
- `mcp_server.py` — MCP tools wrapping core
- Claude skill (`/whatsup`) installed to `~/.claude/skills/`
- End-to-end test: CLI → Telegram group message

### Sprint 2: REST API + Afterburner Hooks
- `server.py` — HTTP server on port 1202
- Wire POST_MERGE_HOOKS in Afterburner sprint-config template
- Add sprint-started and agent-completed event types
- History log: `~/.config/tool-telegram-whatsapp/history/<slug>.jsonl`
- End-to-end test: Afterburner sprint → notification in Telegram group

### Sprint 3: WhatsApp Transport
- `transport/whatsapp.py` — WhatsApp Business Cloud API client
- Register message templates with Meta
- Per-project transport selection in config
- Mixed transport test: one project on Telegram, one on WhatsApp
