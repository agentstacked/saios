"""Evals for lead_intercept. Run with: uv run pytest saios/agents/lead_intercept/evals.py"""
from __future__ import annotations

import pytest

from saios.harness import load_config
from saios.agents.lead_intercept.agent import build


HOT_LEAD = """
name: Maya Chen
email: maya@designstudio.io
company: 6-person design studio, $40k MRR
budget: $8-12k for the right partner
ask: We need to automate our client onboarding flow before our Q3 hire pause.
        Specifically: contract → kickoff brief → resource provisioning. Want to start in 2 weeks.
"""

COLD_LEAD = """
name: hello there
email: ceo@growth-hacker.biz
company: (unspecified)
budget: (no budget mentioned)
ask: Hi! Loved your post. Could you do a free audit of our funnel?
"""

SPAM = """
name: SEO Solutions Pro
email: outreach@bulkmail.example
company: (unspecified)
ask: I noticed your website could rank higher. Would you like a quote for SEO services?
"""


@pytest.fixture
def agent():
    return build(load_config())


@pytest.mark.skip(reason="enable when ANTHROPIC_API_KEY is set and you want to spend ~$0.01/run")
def test_hot_lead_classified_hot(agent):
    out = agent.run(HOT_LEAD)
    assert "HOT" in out.upper()


@pytest.mark.skip(reason="enable when API key is set")
def test_cold_lead_not_hot(agent):
    out = agent.run(COLD_LEAD)
    assert "HOT" not in out.upper()


@pytest.mark.skip(reason="enable when API key is set")
def test_spam_classified_cold(agent):
    out = agent.run(SPAM)
    assert "COLD" in out.upper()
