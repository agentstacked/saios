from __future__ import annotations

from pathlib import Path

from saios.harness import Agent, Config
from saios.tools import build_notion_tools


def build(config: Config) -> Agent:
    prompt = (Path(__file__).parent / "prompt.md").read_text(encoding="utf-8")
    return Agent(
        name="lead_intercept",
        system_prompt=prompt,
        tools=build_notion_tools(),
        config=config,
        max_iterations=10,
    )
