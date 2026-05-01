"""Run the Inbox Triage agent.

  uv run python scripts/run_inbox_triage.py
"""
from __future__ import annotations

from saios.harness import load_config
from saios.agents.inbox_triage.agent import build


def main() -> None:
    config = load_config()
    agent = build(config)
    summary = agent.run("Triage today's inbox.")
    print("\n=== TRIAGE SUMMARY ===\n")
    print(summary)


if __name__ == "__main__":
    main()
