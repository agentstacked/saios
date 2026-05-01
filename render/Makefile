.PHONY: render-inbox render-lead render-content render-all clean check-deps

check-deps:
	@command -v vhs >/dev/null 2>&1 || { echo "Install VHS: https://github.com/charmbracelet/vhs"; exit 1; }
	@command -v ffmpeg >/dev/null 2>&1 || { echo "Install ffmpeg"; exit 1; }
	@test -d remotion/node_modules || { echo "Run: cd remotion && npm install"; exit 1; }

render-inbox: check-deps
	uv run python scripts/render_brief.py briefs/inbox_triage_walkthrough.md

render-lead: check-deps
	uv run python scripts/render_brief.py briefs/lead_intercept_walkthrough.md

render-content: check-deps
	uv run python scripts/render_brief.py briefs/content_multiplier_walkthrough.md

render-all: render-inbox render-lead render-content

clean:
	rm -rf out/ tapes/*.mp4 remotion/out/
