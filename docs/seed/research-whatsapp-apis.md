# WhatsApp API Research — March 2026

## Transport Options Evaluated

### 1. WhatsApp Business Cloud API (Official — CHOSEN for Phase 2)
- **Provider:** Meta (official)
- **Ban risk:** None
- **Cost:** Free tier 1,000 service conversations/month
- **Groups API:** Available since Oct 2025. Max 8 participants per group. Supports programmatic creation.
- **Requirements:** Meta Business account, business verification (3-7 days), dedicated phone number
- **Constraint:** Groups API requires Official Business Account (green tick) — hard for solo devs
- **Templates:** Outbound-first messages require pre-approved message templates

### 2. Whapi.cloud (Third-party)
- **Provider:** Whapi.cloud
- **Cost:** $35/mo flat, no per-message fees
- **Protocol:** Uses whatsmeow (unofficial) under the hood
- **Ban risk:** HIGH — same unofficial protocol, same detection risk
- **Features:** Full group management, clean REST API, Python examples

### 3. whatsapp-mcp (lharries/whatsapp-mcp)
- **Creator:** Luke Harries, Head of Growth at ElevenLabs (London)
- **Stars:** 3k+ on GitHub
- **Not official** — community project
- **Protocol:** whatsmeow (Go library, reverse-engineered WhatsApp Web multi-device protocol)
- **Ban risk:** HIGH — Meta actively detecting unofficial automation even at low volume
- **Features:** MCP server, SQLite storage, group messaging, personal account via QR code

### 4. NanoClaw (lightweight OpenClaw alternative)
- **Size:** ~3,900 lines, 15 files
- **Built on:** Anthropic Agents SDK
- **WhatsApp:** Multi-device web protocol (same ban risk)
- **Features:** Container isolation, session memory, per-group context
- **Overkill** for just a messaging tool

## Meta's 2026 Policy Changes
- Meta changed WhatsApp terms (effective Jan 15, 2026) to ban third-party AI assistants
- Targets general-purpose chatbots (ChatGPT, Perplexity on WhatsApp)
- Business-specific bots for support, notifications, bookings still ALLOWED
- Ban currently PAUSED due to EU/Italy regulatory pushback
- Unofficial protocol users (whatsmeow, Baileys) getting "account at risk" warnings

## Decision
- **Phase 1:** Telegram Bot API (free, official, instant setup, zero ban risk)
- **Phase 2:** WhatsApp Business Cloud API when Business verification comes through
- **Transport-agnostic architecture** allows both simultaneously

## Sources
- https://developers.facebook.com/documentation/business-messaging/whatsapp/groups
- https://whapi.cloud/
- https://github.com/lharries/whatsapp-mcp
- https://github.com/qwibitai/nanoclaw
- https://respond.io/blog/whatsapp-general-purpose-chatbots-ban
- https://chatarmin.com/en/blog/whatsapp-cloudapi
