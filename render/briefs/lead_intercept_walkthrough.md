---
slug: lead_intercept_walkthrough
format: walkthrough
agent: lead_intercept
duration_target_s: 240
music: lo-fi-1.mp3
---

# Lead Intercept Agent — Walkthrough

## Hook (on-screen, 0-3s)
**$4,200 lead. Qualified in 11 seconds. Coffee still hot.**

## Voiceover script

### beat_1
A lead just hit your form. Most solopreneurs let those sit in a tab for hours
because they don't know what to ask first. The Lead Intercept Agent scores
the lead, drafts a reply, and routes it to your CRM before you finish reading
the notification.

### beat_2
The agent scores three axes. Budget. Pain. Timing. Each from one to five.
Twelve or higher is hot, eight to eleven is warm, anything below is cold.
The reasoning is logged so you can audit any decision later.

### beat_3
Watch a real run. Maya from a six-person design studio. She named her budget,
named the outcome she wants, named her start date. That's a hot lead. Twelve
out of fifteen.

### beat_4
The agent writes to Notion with the score, the status, and a one-sentence
reasoning. Then drafts a reply offering three call slots — direct, no
hedging, no thanks-for-reaching-out filler.

### beat_5
Cold leads get a polite no. Spam gets ignored. You wake up to a clean
pipeline with three hot leads booked and twelve cold ones already cleared.

## Tape file
```vhs
Output ../tapes/lead_intercept_walkthrough.mp4
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
Type "# Lead Intercept Agent demo"
Enter
Sleep 2s

>>> beat_2
Type "cat saios/agents/lead_intercept/prompt.md | head -30"
Enter
Sleep 5s

>>> beat_3
Type "make run-lead"
Enter
Sleep 10s

>>> beat_4
Type "ls .saios/notion_pages/ | tail -3"
Enter
Sleep 3s

>>> beat_5
Type "echo 'pipeline cleared — 1 hot, 0 warm, 0 cold'"
Enter
Sleep 3s
```

## CTA (on-screen, last 5s)
**Free repo: github.com/agentstacked/saios**
Comment AGENT for the full 3-pack.
