"""Filesystem tools — for the Content Multiplier agent to write outputs."""
from __future__ import annotations

from pathlib import Path

from saios.harness.agent import Tool, ToolResult

OUT_DIR = Path("./.saios/outputs")


def _write_output(filename: str, content: str) -> ToolResult:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    safe = filename.replace("..", "").replace("/", "_").replace("\\", "_")
    path = OUT_DIR / safe
    path.write_text(content, encoding="utf-8")
    return ToolResult(content=f"Wrote {len(content)} bytes to {path}")


def _read_input(path: str) -> ToolResult:
    p = Path(path)
    if not p.exists():
        return ToolResult(content=f"File not found: {path}", is_error=True)
    return ToolResult(content=p.read_text(encoding="utf-8"))


def build_fs_tools() -> list[Tool]:
    return [
        Tool(
            name="read_input",
            description="Read a local text file (long-form post, transcript, brief, etc).",
            input_schema={
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
            handler=_read_input,
        ),
        Tool(
            name="write_output",
            description="Write a text output to ./.saios/outputs/<filename>. Use one call per platform.",
            input_schema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["filename", "content"],
            },
            handler=_write_output,
        ),
    ]
