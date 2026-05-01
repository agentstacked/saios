from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

import anthropic

from saios.harness.config import Config
from saios.harness.cost_guard import CostGuard
from saios.harness.logging import get_logger


@dataclass
class ToolResult:
    content: str
    is_error: bool = False


class ToolHandler(Protocol):
    def __call__(self, **kwargs: Any) -> ToolResult: ...


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: ToolHandler

    def to_anthropic(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }


@dataclass
class Agent:
    name: str
    system_prompt: str
    tools: list[Tool]
    config: Config
    model: str | None = None
    max_iterations: int = 10
    require_human_approval: bool = False

    _client: anthropic.Anthropic = field(init=False)
    _cost: CostGuard = field(init=False)
    _log: Any = field(init=False)
    _tools_by_name: dict[str, Tool] = field(init=False)

    def __post_init__(self) -> None:
        self._client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
        self._cost = CostGuard(
            agent_name=self.name,
            state_dir=self.config.state_dir,
            per_run_cap=self.config.per_run_usd_cap,
            daily_cap=self.config.daily_usd_cap,
        )
        self._log = get_logger(self.name, self.config.log_level, self.config.log_dir)
        self._tools_by_name = {t.name: t for t in self.tools}
        if self.model is None:
            self.model = self.config.default_model

    def run(self, user_message: str, approve: Callable[[str, dict], bool] | None = None) -> str:
        self._log.info(f"[{self.name}] start — model={self.model}")
        messages: list[dict[str, Any]] = [{"role": "user", "content": user_message}]

        for step in range(self.max_iterations):
            response = self._client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                tools=[t.to_anthropic() for t in self.tools],
                messages=messages,
            )

            cost = self._cost.add_usage(
                self.model,
                response.usage.input_tokens,
                response.usage.output_tokens,
            )
            self._log.debug(
                f"[{self.name}] step={step} stop={response.stop_reason} "
                f"in={response.usage.input_tokens} out={response.usage.output_tokens} "
                f"cost=${cost:.4f} run_total=${self._cost.run_usd:.4f}"
            )

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                final = "".join(
                    b.text for b in response.content if getattr(b, "type", "") == "text"
                )
                self._log.info(f"[{self.name}] done — ${self._cost.run_usd:.4f}")
                return final

            if response.stop_reason != "tool_use":
                self._log.warning(f"[{self.name}] unexpected stop_reason: {response.stop_reason}")
                return ""

            tool_results: list[dict[str, Any]] = []
            for block in response.content:
                if getattr(block, "type", "") != "tool_use":
                    continue
                tool = self._tools_by_name.get(block.name)
                if tool is None:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": f"Unknown tool: {block.name}",
                        "is_error": True,
                    })
                    continue

                if self.require_human_approval and approve is not None:
                    if not approve(block.name, dict(block.input)):
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": "Human declined this action.",
                            "is_error": True,
                        })
                        continue

                self._log.info(f"[{self.name}] → {block.name}({_short(block.input)})")
                try:
                    result = tool.handler(**dict(block.input))
                except Exception as e:
                    result = ToolResult(content=f"Tool error: {e}", is_error=True)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result.content,
                    "is_error": result.is_error,
                })

            messages.append({"role": "user", "content": tool_results})

        self._log.warning(f"[{self.name}] hit max_iterations={self.max_iterations}")
        return ""


def _short(d: dict, n: int = 80) -> str:
    s = ", ".join(f"{k}={v!r}" for k, v in d.items())
    return s if len(s) <= n else s[:n] + "..."
