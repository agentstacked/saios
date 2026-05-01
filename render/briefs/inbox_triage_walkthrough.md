---
slug: inbox_triage_walkthrough
format: walkthrough          # walkthrough (16:9, 4-7min) | reel (9:16, 18-25s)
agent: inbox_triage
duration_target_s: 240
music: lo-fi-1.mp3
---

# Inbox Triage Agent — Walkthrough

## Hook (on-screen, 0-3s)
**87 unread emails. 4 actually need you.**

## Voiceover script
[The brief is split into voiceover beats. Each beat aligns with a `>>>` marker
in the tape file below. The render script splits the VO into segments and
stitches them to the video timing.]

### beat_1
Most solopreneurs spend an hour every morning sorting email. The Inbox Triage
Agent does it in eleven seconds, and it's better than you at not getting
distracted by newsletters.

### beat_2
Here's how it works. The agent has four tools: list, read, draft, and label.
You give it one instruction — triage today's inbox — and it loops until done.

### beat_3
Watch what happens. It pulls the unread threads, reads each one, classifies
into urgent, FYI, newsletter, or reply-draft. The reasoning is visible the
whole time.

### beat_4
For anything that needs a reply, it drafts in your voice. Notice it doesn't
send — drafts only. The human is in the loop until you decide otherwise.

### beat_5
Final summary. Three urgent items, one of them a payment failure. Two reply
drafts ready in your inbox. Eighteen newsletters labeled and out of sight.
Fifteen seconds of agent time. Thirty minutes of your morning back.

## Tape file (drives the terminal recording)
```vhs
Output ../tapes/inbox_triage_walkthrough.mp4
Set FontSize 16
Set Width 1920
Set Height 1080
Set Theme "Catppuccin Mocha"

Hide
Type "cd ../.."
Enter
Type "clear"
Enter
Show

>>> beat_1
Type "# Inbox Triage Agent demo"
Enter
Sleep 2s

>>> beat_2
Type "cat saios/agents/inbox_triage/prompt.md | head -20"
Enter
Sleep 5s

>>> beat_3
Type "make run-inbox"
Enter
Sleep 12s

>>> beat_4
Type "ls .saios/drafts/"
Enter
Sleep 3s
Type "cat .saios/drafts/thread_003.txt"
Enter
Sleep 5s

>>> beat_5
Type "echo 'done — 3 urgent, 2 drafts, 18 newsletters'"
Enter
Sleep 3s
```

## CTA (on-screen, last 5s)
**Free repo: github.com/agentstacked/saios**
Comment AGENT for the full 3-pack.
