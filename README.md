# SAIOS Starter — 3 AI Agents That Replaced My VA

Free 3-agent starter pack from the [Solopreneur AI Operating System](https://example.com/saios).

Three production-grade AI agents you can deploy in one command:

1. **Inbox Triage Agent** — reads Gmail, drafts replies in your voice, surfaces only what needs you
2. **Lead Intercept Agent** — qualifies inbound leads, routes to your CRM, books calls
3. **Content Multiplier Agent** — one long-form post → 6 platforms, on-brand

Built on the Anthropic Python SDK using Claude Agent SDK patterns: real tool use, real memory, real cost guards. No no-code workflows, no Zapier glue.

## Quick start (3 minutes)

```bash
git clone https://github.com/agentstacked/saios.git
cd saios
cp .env.example .env          # fill in ANTHROPIC_API_KEY
make install                  # uv sync
make run-inbox                # try it on a sample inbox
```

That's it. Each agent runs standalone — pick the one that hurts most and start there.

## What's inside

```
saios/
├── harness/        Base Agent class, tool-use loop, cost guard, logging
├── tools/          MCP-style tool wrappers (Gmail, Notion, HTTP, ...)
└── agents/         The three agents — prompt + tools + evals per folder
```

## Cost guard

Every agent has a per-run + per-day USD cap. Hit the cap, the agent stops cleanly and logs a Slack-able warning. Set in `.env`:

```
DAILY_USD_CAP=2.00
PER_RUN_USD_CAP=0.25
```

## What you bring

- An Anthropic API key (~$5–20/mo at typical use)
- Python 3.11+
- `uv` (`curl -LsSf https://astral.sh/uv/install.sh | sh` — or use pip)

## Bonus — `render/` (the pipeline that made the demo videos)

The walkthrough videos for these agents are produced by a fully autonomous pipeline in [`render/`](./render). VHS for terminal recording, ElevenLabs for AI voiceover, Remotion for composition. **No manual recording, no manual editing — write a Markdown brief, run `make render-inbox`, get an MP4.** See [`render/README.md`](./render/README.md).

## What's NOT in this starter (it's in SAIOS)

- 9 more agents (Calendar Concierge, Proposal, Money Ops, Meeting → Action, DM Concierge, Idea Vault, Testimonial Harvester, Research, Wrap-Up)
- The Operator Agent — the meta-agent that delegates to the others
- Notion control panel + dashboard
- Walkthrough Library (12 AI-rendered videos), Operator's Playbook, eval pack
- Managed hosting option

→ [Founders pricing](https://example.com/saios) — $147 until 100 buyers, then $247.

## License

MIT. Use these agents however you want. If you ship them to clients, send screenshots — I post the best ones.
