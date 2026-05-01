from __future__ import annotations

from pathlib import Path

from saios.harness import Agent, Config
from saios.tools import build_fs_tools


def build(config: Config) -> Agent:
    prompt = (Path(__file__).parent / "prompt.md").read_text(encoding="utf-8")
    return Agent(
        name="content_multiplier",
        system_prompt=prompt,
        tools=build_fs_tools(),
        config=config,
        max_iterations=15,
    )
