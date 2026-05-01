"""Notion tools — stubbed. Replace _create_page with a real Notion API call when NOTION_API_KEY is set.

For dev, writes to ./.saios/notion_pages/*.json so the agent can run without a Notion workspace.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

from saios.harness.agent import Tool, ToolResult

PAGES_DIR = Path("./.saios/notion_pages")


def _create_page(database: str, title: str, properties: dict, body: str = "") -> ToolResult:
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    page_id = uuid.uuid4().hex[:12]
    payload = {
        "id": page_id,
        "database": database,
        "title": title,
        "properties": properties,
        "body": body,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    (PAGES_DIR / f"{page_id}.json").write_text(json.dumps(payload, indent=2))
    return ToolResult(content=f"Created Notion page {page_id} in {database}")


def _query(database: str, filter_text: str = "") -> ToolResult:
    if not PAGES_DIR.exists():
        return ToolResult(content="[]")
    rows = []
    for p in sorted(PAGES_DIR.glob("*.json")):
        data = json.loads(p.read_text())
        if data.get("database") != database:
            continue
        if filter_text and filter_text.lower() not in json.dumps(data).lower():
            continue
        rows.append(data)
    return ToolResult(content=json.dumps(rows, indent=2))


def build_notion_tools() -> list[Tool]:
    return [
        Tool(
            name="notion_create_page",
            description="Create a page in a Notion database. Properties is a key/value dict matching the database schema.",
            input_schema={
                "type": "object",
                "properties": {
                    "database": {"type": "string"},
                    "title": {"type": "string"},
                    "properties": {"type": "object"},
                    "body": {"type": "string"},
                },
                "required": ["database", "title", "properties"],
            },
            handler=_create_page,
        ),
        Tool(
            name="notion_query",
            description="Query a Notion database with optional substring filter.",
            input_schema={
                "type": "object",
                "properties": {
                    "database": {"type": "string"},
                    "filter_text": {"type": "string"},
                },
                "required": ["database"],
            },
            handler=_query,
        ),
    ]
