# Render Pipeline

The autonomous video pipeline that produces walkthrough videos and IG Reels for SAIOS — **no live recording, no manual editing.**

```
brief.md  →  VHS .tape  →  terminal.mp4  ┐
                                          ├─→  Remotion compose  →  final.mp4
brief.md  →  ElevenLabs API → vo.mp3      ┘
```

## Stack

| Layer | Tool | Install |
|---|---|---|
| Terminal recording | [VHS](https://github.com/charmbracelet/vhs) | `scoop install vhs` (Win) / `brew install vhs` (Mac) |
| AI voiceover | [ElevenLabs API](https://elevenlabs.io) | `pip install elevenlabs` (already in pyproject) |
| Video composition | [Remotion](https://remotion.dev) | `cd remotion && npm install` |
| Final mux | ffmpeg | `scoop install ffmpeg` / `brew install ffmpeg` |

## One-time setup (~30 min)

1. Install VHS, ffmpeg, and Node 20+
2. Sign up at [elevenlabs.io](https://elevenlabs.io) — Creator tier ($22/mo) for voice cloning
3. Record a clean ~3 min audio sample of yourself reading varied text. Upload to ElevenLabs → "Voices" → "Add Voice" → "Instant Voice Clone"
4. Copy the resulting voice ID into `.env`:
   ```
   ELEVENLABS_API_KEY=...
   ELEVENLABS_VOICE_ID=...
   ```
5. `cd remotion && npm install` (one-time, takes ~2 min)

## Per-video workflow

```bash
# 1. Write a brief in render/briefs/<name>.md
#    (See briefs/inbox_triage_walkthrough.md for the format)

# 2. Render
make render-inbox

# 3. Output lands in render/out/inbox_triage_walkthrough.mp4
```

That's it. Same input = same output, every time. Iterate on the brief, not on a video timeline.

## What's in here

- `tapes/` — VHS `.tape` scripts (declarative terminal recordings)
- `briefs/` — Markdown briefs that drive a full render (hook + voiceover + commands)
- `scripts/` — Glue scripts (ElevenLabs voiceover, brief-to-tape compiler)
- `remotion/` — React video templates (9:16 Reel, 16:9 walkthrough)
- `out/` — Final MP4s (gitignored)
