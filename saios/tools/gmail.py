"""Gmail tools — stubbed. Wire to the Gmail API or an MCP server before production.

For dev/eval, the stubs read from ./fixtures/gmail/*.json so the agent can run end-to-end
without an OAuth dance.
"""
from __future__ import annotations

import json
from pathlib import Path

from saios.harness.agent import Tool, ToolResult

FIXTURE_DIR = Path("fixtures/gmail")


def _list_unread(max_results: int = 20) -> ToolResult:
    if not FIXTURE_DIR.exists():
        return ToolResult(content="[]")
    items = []
    for p in sorted(FIXTURE_DIR.glob("*.json"))[:max_results]:
        items.append(json.loads(p.read_text()))
    return ToolResult(content=json.dumps(items, indent=2))


def _get_thread(thread_id: str) -> ToolResult:
    p = FIXTURE_DIR / f"{thread_id}.json"
    if not p.exists():
        return ToolResult(content=f"Thread {thread_id} not found", is_error=True)
    return ToolResult(content=p.read_text())


def _draft_reply(thread_id: str, body: str) -> ToolResult:
    drafts = Path("./.saios/drafts")
    drafts.mkdir(parents=True, exist_ok=True)
    (drafts / f"{thread_id}.txt").write_text(body)
    return ToolResult(content=f"Draft saved for thread {thread_id}")


def _label(thread_id: str, label: str) -> ToolResult:
    return ToolResult(content=f"Labeled {thread_id} as {label}")


def build_gmail_tools() -> list[Tool]:
    return [
        Tool(
            name="gmail_list_unread",
            description="List unread Gmail threads with subject, snippet, sender. Returns JSON array.",
            input_schema={
                "type": "object",
                "properties": {
                    "max_results": {"type": "integer", "default": 20},
                },
            },
            handler=_list_unread,
        ),
        Tool(
            name="gmail_get_thread",
            description="Fetch the full body of a thread by id.",
            input_schema={
                "type": "object",
                "properties": {"thread_id": {"type": "string"}},
                "required": ["thread_id"],
            },
            handler=_get_thread,
        ),
        Tool(
            name="gmail_draft_reply",
            description="Save a draft reply on a thread (does NOT send). Body should be in the user's voice.",
            input_schema={
                "type": "object",
                "properties": {
                    "thread_id": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["thread_id", "body"],
            },
            handler=_draft_reply,
        ),
        Tool(
            name="gmail_label",
            description="Apply a label to a thread (e.g. 'Triaged/Urgent', 'Triaged/FYI', 'Triaged/Newsletter').",
            input_schema={
                "type": "object",
                "properties": {
                    "thread_id": {"type": "string"},
                    "label": {"type": "string"},
                },
                "required": ["thread_id", "label"],
            },
            handler=_label,
        ),
    ]
