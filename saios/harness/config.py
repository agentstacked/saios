from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    anthropic_api_key: str
    default_model: str
    fast_model: str
    daily_usd_cap: float
    per_run_usd_cap: float
    log_level: str
    log_dir: Path
    state_dir: Path
    gmail_oauth_path: Path | None
    notion_api_key: str | None
    slack_webhook_url: str | None


def load_config(env_file: str | Path = ".env") -> Config:
    load_dotenv(env_file)

    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key or api_key.startswith("sk-ant-...") or api_key == "":
        raise SystemExit(
            "ANTHROPIC_API_KEY missing or unset. Edit .env and set a real key."
        )

    log_dir = Path(os.environ.get("LOG_DIR", "./.saios/logs"))
    state_dir = Path(os.environ.get("STATE_DIR", "./.saios/state"))
    log_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    gmail_oauth = os.environ.get("GMAIL_OAUTH_PATH")
    notion_key = os.environ.get("NOTION_API_KEY") or None
    slack_url = os.environ.get("SLACK_WEBHOOK_URL") or None

    return Config(
        anthropic_api_key=api_key,
        default_model=os.environ.get("DEFAULT_MODEL", "claude-sonnet-4-6"),
        fast_model=os.environ.get("FAST_MODEL", "claude-haiku-4-5-20251001"),
        daily_usd_cap=float(os.environ.get("DAILY_USD_CAP", "2.00")),
        per_run_usd_cap=float(os.environ.get("PER_RUN_USD_CAP", "0.25")),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
        log_dir=log_dir,
        state_dir=state_dir,
        gmail_oauth_path=Path(gmail_oauth) if gmail_oauth else None,
        notion_api_key=notion_key,
        slack_webhook_url=slack_url,
    )
