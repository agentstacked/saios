from __future__ import annotations

from pathlib import Path

from saios.harness import Agent, Config
from saios.tools import build_gmail_tools


def build(config: Config) -> Agent:
    prompt = (Path(__file__).parent / "prompt.md").read_text(encoding="utf-8")
    return Agent(
        name="inbox_triage",
        system_prompt=prompt,
        tools=build_gmail_tools(),
        config=config,
        max_iterations=30,
    )
