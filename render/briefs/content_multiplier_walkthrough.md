---
slug: content_multiplier_walkthrough
format: walkthrough
agent: content_multiplier
duration_target_s: 240
music: lo-fi-1.mp3
---

# Content Multiplier Agent — Walkthrough

## Hook (on-screen, 0-3s)
**One blog post. Six platforms. Thirty seconds.**

## Voiceover script

### beat_1
You write one long-form post a week. You should be posting it six times,
once per platform, each tailored. Most people don't because the editing is
boring. The Content Multiplier Agent does it for you.

### beat_2
Feed it a Markdown file. The agent identifies the core idea, then writes six
platform-native versions. Instagram carousel. Reel script. LinkedIn post.
Twitter thread. Email. YouTube short.

### beat_3
Watch a real run. Source post: why I stopped hiring VAs. Three hundred
words. The agent reads it, anchors on the core idea, and writes each output
to a separate file.

### beat_4
Notice the constraints. No em dashes. No corporate filler. Hooks under eight
words. Each output stands alone — assume the reader hasn't seen the others.
That's not a vibe, those are rules in the system prompt.

### beat_5
Six files in your outputs folder, ready to schedule. The whole run cost two
cents in API calls and finished while you were still on your first coffee.

## Tape file
```vhs
Output ../tapes/content_multiplier_walkthrough.mp4
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
Type "# Content Multiplier Agent demo"
Enter
Sleep 2s

>>> beat_2
Type "cat fixtures/sample_post.md"
Enter
Sleep 6s

>>> beat_3
Type "make run-content"
Enter
Sleep 18s

>>> beat_4
Type "ls .saios/outputs/"
Enter
Sleep 3s

>>> beat_5
Type "head -20 .saios/outputs/instagram_carousel.md"
Enter
Sleep 5s
```

## CTA (on-screen, last 5s)
**Free repo: github.com/agentstacked/saios**
Comment AGENT for the full 3-pack.
