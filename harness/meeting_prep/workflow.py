from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MeetingPrepBrief:
    event: dict[str, Any]
    prior_discussion: tuple[str, ...]
    open_commitments: tuple[dict[str, Any], ...]
    decisions: tuple[str, ...]
    source_paths: tuple[Path, ...]


DEFAULT_CALENDAR = Path("examples/calendar.json")
DEFAULT_TRANSCRIPT = Path("examples/meeting-transcript.md")
DEFAULT_COMMITMENTS = Path("agents/demo/memory/commitments.jsonl")


def build_meeting_prep(repo_root: Path, event_id: str | None = None) -> MeetingPrepBrief:
    calendar_path = repo_root / DEFAULT_CALENDAR
    transcript_path = repo_root / DEFAULT_TRANSCRIPT
    commitments_path = repo_root / DEFAULT_COMMITMENTS

    events = json.loads(calendar_path.read_text())
    event = _select_event(events, event_id)
    transcript = transcript_path.read_text()
    commitments = _read_commitments(commitments_path)

    open_commitments = tuple(
        item for item in commitments if item.get("status") == "open"
    )
    discussion = _extract_discussion(transcript)
    decisions = _derive_decisions(event, open_commitments, discussion)

    return MeetingPrepBrief(
        event=event,
        prior_discussion=discussion,
        open_commitments=open_commitments,
        decisions=decisions,
        source_paths=(DEFAULT_CALENDAR, DEFAULT_TRANSCRIPT, DEFAULT_COMMITMENTS),
    )


def render_brief(brief: MeetingPrepBrief) -> str:
    event = brief.event
    lines: list[str] = []
    lines.append("Meeting Prep")
    lines.append("")
    lines.append(f"Meeting: {event['title']}")
    lines.append(f"When: {event['starts_at']} to {event['ends_at']}")
    lines.append(f"Attendees: {', '.join(event.get('attendees', []))}")
    lines.append("")
    lines.append("What happened last time")
    for item in brief.prior_discussion:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Open commitments")
    for item in brief.open_commitments:
        lines.append(
            f"- {item['owner']} by {item['due']}: {item['summary']} "
            f"({item['id']})"
        )
    if not brief.open_commitments:
        lines.append("- None found.")
    lines.append("")
    lines.append("Decisions to make")
    for item in brief.decisions:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Sources")
    for path in brief.source_paths:
        lines.append(f"- {path}")
    return "\n".join(lines) + "\n"


def _select_event(events: list[dict[str, Any]], event_id: str | None) -> dict[str, Any]:
    if event_id is None:
        if not events:
            raise ValueError("calendar fixture has no events")
        return events[0]
    for event in events:
        if event.get("id") == event_id:
            return event
    raise ValueError(f"event not found: {event_id}")


def _read_commitments(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _extract_discussion(transcript: str) -> tuple[str, ...]:
    items: list[tuple[str, str]] = []
    current_speaker: str | None = None
    current_parts: list[str] = []

    def flush() -> None:
        nonlocal current_speaker, current_parts
        if current_speaker and current_parts:
            items.append((current_speaker, " ".join(current_parts)))
        current_speaker = None
        current_parts = []

    for raw_line in transcript.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            flush()
            continue
        if _looks_like_speaker_line(line):
            flush()
            speaker, statement = line.split(":", 1)
            current_speaker = speaker.strip()
            current_parts = [statement.strip()]
            continue
        if current_speaker:
            current_parts.append(line)
    flush()

    return tuple(
        f"{speaker}: {_clean_statement(statement)}"
        for speaker, statement in items
        if statement.strip()
    )


def _derive_decisions(
    event: dict[str, Any],
    commitments: tuple[dict[str, Any], ...],
    discussion: tuple[str, ...],
) -> tuple[str, ...]:
    decisions = [
        f"Confirm whether '{event['title']}' is ready to move forward.",
    ]
    for item in commitments:
        decisions.append(f"Check whether {item['owner']} completed {item['id']}.")
    if any("synthetic" in item.lower() for item in discussion):
        decisions.append("Verify the demo stays inside synthetic/public-safe data.")
    return tuple(decisions)


def _clean_statement(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _looks_like_speaker_line(line: str) -> bool:
    if ":" not in line:
        return False
    speaker, statement = line.split(":", 1)
    if not statement.strip():
        return False
    if speaker.lower() in {"date", "source", "note"}:
        return False
    words = speaker.split()
    return 1 <= len(words) <= 4 and all(word[:1].isupper() for word in words)
