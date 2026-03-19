---
name: whatsup
description: Send messages and notifications to project group chats via Telegram/WhatsApp
trigger: When user says /whatsup
---

# whatsup — Project Group Chat Messaging

Send checkins, notifications, and status checks to project group chats.

## Usage

### Send a checkin message
```
/whatsup <project> <message>
```
Call the `send_checkin` MCP tool with:
- `slug`: the project slug (first argument)
- `summary`: the message text (remaining arguments)

Example: `/whatsup grassyknoll Deployed auth service to staging`

### Check status
```
/whatsup status
```
Call the `whatsup_status` MCP tool (no arguments). Returns transport health for all configured transports.

### List projects
```
/whatsup projects
```
Call the `whatsup_projects` MCP tool (no arguments). Returns all configured projects with their transport and group info.

## MCP Tool Mapping

| Command | MCP Tool | Parameters |
|---------|----------|------------|
| `/whatsup <project> <message>` | `send_checkin` | `slug`, `summary` |
| `/whatsup status` | `whatsup_status` | _(none)_ |
| `/whatsup projects` | `whatsup_projects` | _(none)_ |

## MCP Server

Server name: `tool-telegram-whatsapp`
Transport: stdio
Entry point: `python3 -m whatsup.mcp_server`
