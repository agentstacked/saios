"""
Render a video from a Markdown brief.

  uv run python scripts/render_brief.py briefs/inbox_triage_walkthrough.md

Pipeline:
  1. Parse brief (frontmatter + voiceover beats + tape block + hook + CTA)
  2. Extract tape block, write to render/tapes/<slug>.tape, run `vhs <tape>` → terminal.mp4
  3. For each VO beat, call ElevenLabs → MP3, then concat with ffmpeg → vo.mp3
  4. Write Remotion props.json (slug, hook, cta, durations, paths)
  5. Run `npx remotion render` → out/<slug>.mp4

This is the orchestrator. Each step is a separate function so individual
stages can be re-run when iterating.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

RENDER_ROOT = Path(__file__).parent.parent.resolve()
TAPES_DIR = RENDER_ROOT / "tapes"
OUT_DIR = RENDER_ROOT / "out"
REMOTION_DIR = RENDER_ROOT / "remotion"
VO_DIR = RENDER_ROOT / "out" / "_voiceover"


@dataclass
class Brief:
    slug: str
    format: str
    agent: str
    duration_target_s: int
    music: str
    hook: str
    cta: str
    beats: dict[str, str] = field(default_factory=dict)
    tape: str = ""


def parse_brief(path: Path) -> Brief:
    text = path.read_text(encoding="utf-8")

    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not fm_match:
        raise ValueError(f"{path}: missing frontmatter")
    fm_raw, body = fm_match.group(1), fm_match.group(2)

    if yaml is None:
        fm = dict(line.split(":", 1) for line in fm_raw.strip().splitlines() if ":" in line)
        fm = {k.strip(): v.strip().strip('"').split("#")[0].strip() for k, v in fm.items()}
    else:
        fm = yaml.safe_load(fm_raw)

    hook_match = re.search(r"## Hook.*?\n(.*?)(?=\n##|\Z)", body, re.DOTALL)
    hook = (hook_match.group(1).strip() if hook_match else "").strip("*").strip()

    cta_match = re.search(r"## CTA.*?\n(.*?)(?=\n##|\Z)", body, re.DOTALL)
    cta = (cta_match.group(1).strip() if cta_match else "").strip()

    beats: dict[str, str] = {}
    for m in re.finditer(r"### (beat_\w+)\n(.*?)(?=\n###|\n##|\Z)", body, re.DOTALL):
        beats[m.group(1)] = m.group(2).strip()

    tape_match = re.search(r"```vhs\n(.*?)\n```", body, re.DOTALL)
    tape = tape_match.group(1) if tape_match else ""

    return Brief(
        slug=str(fm.get("slug", path.stem)),
        format=str(fm.get("format", "walkthrough")),
        agent=str(fm.get("agent", "")),
        duration_target_s=int(fm.get("duration_target_s", 60)),
        music=str(fm.get("music", "")),
        hook=hook,
        cta=cta,
        beats=beats,
        tape=tape,
    )


def render_terminal(brief: Brief) -> Path:
    TAPES_DIR.mkdir(parents=True, exist_ok=True)
    tape_path = TAPES_DIR / f"{brief.slug}.tape"
    tape_path.write_text(brief.tape, encoding="utf-8")
    print(f"[1/4] vhs {tape_path.name}")
    subprocess.run(["vhs", str(tape_path)], check=True, cwd=TAPES_DIR)
    out_mp4 = TAPES_DIR / f"{brief.slug}_walkthrough.mp4"
    if not out_mp4.exists():
        candidates = list(TAPES_DIR.glob(f"{brief.slug}*.mp4"))
        if candidates:
            out_mp4 = candidates[0]
        else:
            raise FileNotFoundError("VHS produced no MP4")
    return out_mp4


def synthesize_voiceover(brief: Brief) -> tuple[Path, list[float]]:
    """Generate one MP3 per beat, return concatenated MP3 + per-beat durations."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID")
    if not api_key or not voice_id:
        raise SystemExit("Set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID in .env")

    try:
        from elevenlabs.client import ElevenLabs  # type: ignore
    except ImportError:
        raise SystemExit("uv add elevenlabs")

    client = ElevenLabs(api_key=api_key)
    VO_DIR.mkdir(parents=True, exist_ok=True)

    beat_files: list[Path] = []
    durations: list[float] = []
    for name, text in brief.beats.items():
        out = VO_DIR / f"{brief.slug}_{name}.mp3"
        print(f"[2/4] elevenlabs {name} ({len(text)} chars)")
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_turbo_v2_5",
            output_format="mp3_44100_128",
        )
        with open(out, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        beat_files.append(out)
        durations.append(_mp3_duration(out))

    concat = VO_DIR / f"{brief.slug}.mp3"
    list_file = VO_DIR / f"{brief.slug}.txt"
    list_file.write_text("\n".join(f"file '{p.name}'" for p in beat_files))
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-c", "copy", str(concat)],
        check=True, capture_output=True,
    )
    return concat, durations


def _mp3_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def render_remotion(brief: Brief, terminal_mp4: Path, vo_mp3: Path, vo_durations: list[float]) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    props = {
        "slug": brief.slug,
        "format": brief.format,
        "hook": brief.hook,
        "cta": brief.cta,
        "terminalMp4": str(terminal_mp4.resolve()),
        "voiceoverMp3": str(vo_mp3.resolve()),
        "voiceoverBeats": list(brief.beats.keys()),
        "voiceoverDurations": vo_durations,
        "music": brief.music,
    }
    props_path = REMOTION_DIR / "props.json"
    props_path.write_text(json.dumps(props, indent=2))

    out = OUT_DIR / f"{brief.slug}.mp4"
    composition = "Reel" if brief.format == "reel" else "Walkthrough"
    print(f"[3/4] remotion render {composition}")
    subprocess.run(
        ["npx", "--no-install", "remotion", "render", composition,
         str(out), "--props", str(props_path)],
        check=True, cwd=REMOTION_DIR,
    )
    return out


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: render_brief.py <path-to-brief.md>", file=sys.stderr)
        sys.exit(2)

    brief_path = Path(sys.argv[1]).resolve()
    if not brief_path.exists():
        print(f"brief not found: {brief_path}", file=sys.stderr)
        sys.exit(1)

    brief = parse_brief(brief_path)
    print(f"[0/4] {brief.slug} — {brief.format}, {brief.duration_target_s}s, {len(brief.beats)} beats")

    terminal = render_terminal(brief)
    vo, durations = synthesize_voiceover(brief)
    final = render_remotion(brief, terminal, vo, durations)

    print(f"[4/4] done → {final}")


if __name__ == "__main__":
    main()
