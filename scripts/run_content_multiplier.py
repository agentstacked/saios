"""Run the Content Multiplier agent.

  uv run python scripts/run_content_multiplier.py path/to/post.md
"""
from __future__ import annotations

import sys
from pathlib import Path

from saios.harness import load_config
from saios.agents.content_multiplier.agent import build


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: run_content_multiplier.py <path-to-source.md>", file=sys.stderr)
        sys.exit(2)
    src = Path(sys.argv[1]).resolve()
    if not src.exists():
        print(f"file not found: {src}", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    agent = build(config)
    summary = agent.run(f"Multiply the post at {src}")
    print("\n=== MULTIPLIER SUMMARY ===\n")
    print(summary)
    print("\nOutputs in ./.saios/outputs/")


if __name__ == "__main__":
    main()
