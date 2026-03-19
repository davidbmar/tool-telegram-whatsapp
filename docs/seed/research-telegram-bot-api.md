# Telegram Bot API — Phase 1 Transport

## Why Telegram First
- **Official API** — no ban risk, fully supported by Telegram
- **Free** — no per-message fees, no monthly cost
- **Unlimited** — no conversation caps
- **Instant setup** — message @BotFather, get token, done in 5 minutes
- **Full group management** — create groups, add members, send messages programmatically
- **No verification** — no business account, no legal docs, no waiting

## Setup Steps
1. Message @BotFather on Telegram → `/newbot` → get bot token
2. Create Telegram groups for each Afterburner project
3. Add the bot to each group
4. Get group chat IDs (send a message, check `getUpdates` API)
5. Configure in `~/.config/tool-telegram-whatsapp/config.json`

## Key API Endpoints
- `sendMessage` — send text to a group (chat_id + text)
- `getUpdates` — poll for incoming messages
- `createChatInviteLink` — generate invite links
- `getChat` — get group info
- `getChatMemberCount` — member count

## API Base URL
```
https://api.telegram.org/bot<token>/METHOD
```

## Python Integration
Simple `requests` calls — no SDK needed:
```python
requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
              json={"chat_id": group_id, "text": message})
```
