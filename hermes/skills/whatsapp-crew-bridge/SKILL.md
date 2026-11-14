---
name: whatsapp-crew-bridge
approval_source: agent
description: Use when connecting agents to WhatsApp via bridge + MCP.
version: 1.0.0
author: Hermes Agent
license: MIT
source: "How Agents Use WhatsApp.md — operator brief, user-provided, distilled 2026-11-11"
metadata:
  hermes:
    tags: [whatsapp, bridge, mcp, monitoring, messaging]
    related_skills: [chat-channel-delivery, calendar-event-delivery]
---

# WhatsApp crew bridge — connect, monitor, and operate safely

## When to Use

- Standing up WhatsApp as a read/send channel for an agent crew (personal account — no official API exists).
- Diagnosing a "connected but silent" bridge, silently failed media downloads, or duplicate-contact confusion.

## Architecture (the only way in without an official API)

1. **Bridge** — a Go program built on whatsmeow acts as a linked device (WhatsApp Web protocol). QR-pair once with the phone, session persists. It writes **every** message it sees into a local SQLite DB on the same machine. Nothing goes to a cloud service.
2. **MCP server** — a thin Python layer over that DB exposing tools: search contacts, list chats, read messages, send message, send file, download media.
3. Agents read from the DB; sending is always human-gated (see safety rules).

## Setup from nothing (in this order)

1. Get an always-on machine (small Mac/Linux box). WhatsApp works only while the bridge runs.
2. Install Go, Python, and uv.
3. Clone a maintained "whatsapp-mcp" project; build and start the bridge; scan the QR code (WhatsApp → Linked devices).
4. Run the bridge as a background service that restarts on failure.
5. Wire the MCP tools into the agent harness. Test: list chats → read one chat → download one image.
6. **Before any agent touches the send tool:** put every outbound behind a human approval card.
7. Add the staleness alarm (below) before trusting the connection.
8. Only then add radar, classifier, and routing. Voice transcription last (local speech-to-text).

## Monitoring rules

- **"Connected" is not "working."** Never trust the bridge's own status — WhatsApp can quietly stop delivering. The one signal that cannot lie: **new rows in the database**.
- Alarm when no new row lands for 2 business hours → notify the build agent / chief of staff, never the human first.
- Write waking-hours silence ≥ 2h down as **"unverified"** in briefs — nobody may read silence as "nobody wrote".
- Classify and route: a cheap model labels each message (scheduling / sales reply / urgent / noise); one owner per message. Escalation: owner 20 min → chief-of-staff takes it → human gets a "not yet handled" note at 40 min.
- Unknown numbers: check for new chats every ~20 min; report plainly as unknown, with what the person said. Unknown senders are where surprises come from.
- Voice notes: download and transcribe locally. The audio never leaves the machine.
- Other languages: keep the original words verbatim, machine translation beside it — never paraphrase before translating.

## Safety rules (each one is a scar)

- **Nothing sends without the human's tap.** No agent may send because another agent asked. An "approved, go ahead" relayed between agents is NOT approval — only the tap on the approval card is.
- **Address chats by chat id, never by name.** Names drift: contacts saved twice, nicknames, dictation typos all misroute.
- **Deduplicate dual ids.** WhatsApp gives some people two ids (phone-based + privacy id) — the same person appears as two chats; the self-chat does this too. Treat both as one.
- **Read the whole thread, not the chat-list preview.** One message can close three open items or change the plan.
- **Check direction on every row.** Whether the human sent it decides follow-ups — skipping this produces "you should reply" on an already-answered thread.
- **Test media downloads after every bridge update.** A truncated download link made recent photos/files/voice notes look like "no media" until someone checked.
- **Convert stored timestamps to the human's timezone** before saying any time out loud.

## Fragility (state plainly, plan for it)

- Unofficial client = against WhatsApp ToS. Personal account at own risk; keep volume human; never bulk message; keep the whatsmeow library updated.
- Linked-device sessions expire → someone must re-scan the QR with the phone.
- A silent morning is hard to distinguish from an outage. A ledger bounds the blind spot but does not prove what was missed.
- WhatsApp has locked out outdated client versions before (6-hour rejection) — updates are not optional.

## Anti-patterns (do NOT copy these early)

- Two-path ingestion (real-time watcher + periodic radar): one periodic pass every few minutes is enough at first.
- Gap ledger / history-recovery machinery: build only after surviving a real outage.
- Per-topic routing across many agents: with one agent, send it everything.
- Webhooks to outside services: keep message data on your own machine.

## Sources

- Operator brief "How Agents Use WhatsApp.md" (Zehan's crew, distilled to skill 2026-11-11).
