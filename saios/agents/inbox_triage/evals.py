"""Evals for inbox_triage. Run with: uv run pytest saios/agents/inbox_triage/evals.py

These check the system prompt's classification logic against fixture inboxes.
Fill in fixtures/gmail/*.json to make them runnable.
"""
from __future__ import annotations

import pytest

from saios.harness import load_config
from saios.agents.inbox_triage.agent import build


@pytest.fixture
def agent():
    return build(load_config())


@pytest.mark.skip(reason="add fixtures/gmail/*.json with at least one thread per bucket")
def test_classifies_paying_client_as_urgent(agent):
    out = agent.run("Triage today's inbox.")
    assert "Urgent" in out


@pytest.mark.skip(reason="add fixtures/gmail/*.json")
def test_never_sends_just_drafts(agent):
    out = agent.run("Triage today's inbox.")
    assert "sent" not in out.lower()


@pytest.mark.skip(reason="add fixtures/gmail/*.json")
def test_drafts_match_user_voice(agent):
    out = agent.run("Triage today's inbox.")
    assert "I hope this email finds you well" not in out
