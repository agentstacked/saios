"""Evals for content_multiplier."""
from __future__ import annotations

from pathlib import Path

import pytest

from saios.harness import load_config
from saios.agents.content_multiplier.agent import build


SAMPLE_INPUT = """
# Why I Stopped Hiring VAs

Last quarter I spent $4,200 on a virtual assistant. She was great. But I still
spent two hours every Sunday writing her instructions for the week ahead. The
math caught up with me when I built an inbox-triage agent in 90 minutes that
did 80% of what she did, with no instruction-writing, no scheduling, no PTO.

Three things I learned. First, agents beat humans at *deterministic* repetition,
not creative work — pick the boring tasks. Second, the cost guard matters more
than the agent itself; one runaway loop will eat a month of savings. Third,
agents are easier to fire than VAs (you just stop running them) which makes
the experiment cost much lower than people assume.

I'm not anti-VA. I'm anti-paying-someone-to-do-something-deterministic.
"""


@pytest.fixture
def agent():
    return build(load_config())


@pytest.mark.skip(reason="enable when API key is set; ~$0.02 per run on Sonnet")
def test_produces_six_files(tmp_path, agent):
    src = tmp_path / "input.md"
    src.write_text(SAMPLE_INPUT)
    agent.run(f"Multiply the post at {src}")
    out_dir = Path("./.saios/outputs")
    expected = {
        "instagram_carousel.md",
        "instagram_reel_script.md",
        "linkedin_post.md",
        "x_thread.md",
        "email.md",
        "youtube_short_script.md",
    }
    assert expected.issubset({p.name for p in out_dir.glob("*.md")})


@pytest.mark.skip(reason="enable when API key is set")
def test_no_em_dashes(agent):
    out_dir = Path("./.saios/outputs")
    for p in out_dir.glob("*.md"):
        assert "—" not in p.read_text(), f"em-dash found in {p.name}"
