from __future__ import annotations

import json
from datetime import date
from pathlib import Path

# Approximate per-million-token USD prices. Update when Anthropic changes pricing.
# Used only for the local cost guard — the Anthropic invoice is the source of truth.
PRICING = {
    "claude-opus-4-7":             {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6":           {"input":  3.00, "output": 15.00},
    "claude-haiku-4-5-20251001":   {"input":  1.00, "output":  5.00},
}


class CostGuardTripped(RuntimeError):
    pass


class CostGuard:
    def __init__(
        self,
        agent_name: str,
        state_dir: Path,
        per_run_cap: float,
        daily_cap: float,
    ) -> None:
        self.agent_name = agent_name
        self.per_run_cap = per_run_cap
        self.daily_cap = daily_cap
        self.state_path = state_dir / f"cost_{agent_name}.json"
        self.run_usd = 0.0
        self._load()

    def _load(self) -> None:
        today = date.today().isoformat()
        if self.state_path.exists():
            data = json.loads(self.state_path.read_text())
            if data.get("date") == today:
                self.day_usd = float(data.get("usd", 0.0))
                return
        self.day_usd = 0.0
        self._save()

    def _save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps({"date": date.today().isoformat(), "usd": self.day_usd})
        )

    def add_usage(self, model: str, input_tokens: int, output_tokens: int) -> float:
        rates = PRICING.get(model)
        if rates is None:
            cost = 0.0
        else:
            cost = (
                input_tokens * rates["input"] / 1_000_000
                + output_tokens * rates["output"] / 1_000_000
            )
        self.run_usd += cost
        self.day_usd += cost
        self._save()
        if self.run_usd > self.per_run_cap:
            raise CostGuardTripped(
                f"{self.agent_name}: per-run cap ${self.per_run_cap:.2f} exceeded "
                f"(this run: ${self.run_usd:.4f})"
            )
        if self.day_usd > self.daily_cap:
            raise CostGuardTripped(
                f"{self.agent_name}: daily cap ${self.daily_cap:.2f} exceeded "
                f"(today: ${self.day_usd:.4f})"
            )
        return cost
