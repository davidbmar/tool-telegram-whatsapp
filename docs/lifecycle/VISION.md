# Vision: tool-telegram-whatsapp

## Problem Statement
Developers running Afterburner sprints have no way to receive notifications about sprint lifecycle events on their phone. The dashboard requires active watching — you must be at your computer, browser open, to know when agents finish, merges succeed, or tests fail. For multi-agent sprints that run autonomously for 30-60 minutes, this means wasted attention or missed failures. There's no asynchronous notification channel that reaches you wherever you are.

## Target Audience
Solo developers and small teams using the Afterburner sprint framework to run multi-agent coding sprints. They manage multiple consumer projects (e.g., grassyknoll, FSM-generic) and want per-project communication channels where sprint status, manual checkins, and team updates are scoped and searchable. They value lightweight tools over heavy infrastructure.

## Key Differentiators
- **Transport-agnostic:** A single tool that works across Telegram (Phase 1) and WhatsApp (Phase 2), with per-project transport selection. No vendor lock-in.
- **Four interfaces, one core:** CLI for shell scripts and sprint hooks, REST for service integrations, MCP for AI agents (Claude Code), and a Claude skill for natural language usage. Same business logic everywhere.
- **Afterburner-native:** Designed specifically to plug into the POST_MERGE_HOOKS system and sprint lifecycle events. Zero coupling — Afterburner just shells out to the `whatsup` CLI.
- **Tiny footprint:** ~400 lines of Python, two dependencies (`requests` + `mcp`), no database, file-based config.

## Solution Overview
A standalone Python package (`whatsup`) that routes project-scoped messages to group chats via pluggable transport backends. Each Afterburner project maps to a messaging group. Sprint lifecycle events (merge complete, test failure, agent done) automatically post to the right group. Users and Claude Code can also send manual checkins. Telegram ships first (free, instant, official API), with WhatsApp Business Cloud API added later when Meta Business verification is approved.

## Success Criteria
- Sprint merge notifications arrive on phone within 10 seconds of POST_MERGE_HOOK firing.
- `whatsup send <project> <message>` works from CLI, MCP, and `/whatsup` skill with identical behavior.
- Per-project group isolation: messages for grassyknoll never appear in fsm-generic's group.
- Telegram transport fully functional in Phase 1 with 5-minute setup (BotFather → config → done).
- Adding a new transport requires only implementing the 3-method Transport protocol — no changes to core, CLI, MCP, or skill.
