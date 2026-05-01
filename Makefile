.PHONY: install run-inbox run-lead run-content eval clean

install:
	@command -v uv >/dev/null 2>&1 || { echo "Install uv first: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
	uv sync
	@test -f .env || cp .env.example .env
	@echo ""
	@echo "Installed. Edit .env with your ANTHROPIC_API_KEY, then try:"
	@echo "  make run-inbox"

run-inbox:
	uv run python scripts/run_inbox_triage.py

run-lead:
	uv run python scripts/run_lead_intercept.py

run-content:
	uv run python scripts/run_content_multiplier.py

eval:
	uv run pytest saios/agents -v

clean:
	rm -rf .saios __pycache__ .pytest_cache
