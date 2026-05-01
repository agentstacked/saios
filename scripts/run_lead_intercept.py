"""Run the Lead Intercept agent on a sample lead.

  uv run python scripts/run_lead_intercept.py < lead.txt
  uv run python scripts/run_lead_intercept.py     # uses built-in sample
"""
from __future__ import annotations

import sys

from saios.harness import load_config
from saios.agents.lead_intercept.agent import build


SAMPLE = """
name: Maya Chen
email: maya@designstudio.io
company: 6-person design studio, $40k MRR
budget: $8-12k for the right partner
ask: We need to automate our client onboarding flow before Q3.
        Specifically: contract -> kickoff brief -> resource provisioning.
        Want to start in 2 weeks.
"""


def main() -> None:
    payload = sys.stdin.read() if not sys.stdin.isatty() else SAMPLE
    config = load_config()
    agent = build(config)
    decision = agent.run(payload)
    print("\n=== DECISION ===\n")
    print(decision)


if __name__ == "__main__":
    main()
