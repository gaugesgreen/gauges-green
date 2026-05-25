from pathlib import Path

import pytest

from harness.meeting_prep.workflow import build_meeting_prep, render_brief


def test_meeting_prep_builds_source_backed_brief() -> None:
    brief = build_meeting_prep(Path.cwd())
    text = render_brief(brief)

    assert "Meeting Prep" in text
    assert "Riverbend launch review" in text
    assert "What happened last time" in text
    assert "Open commitments" in text
    assert "Morgan Vale by 2030-04-15" in text
    assert "Riley Chen by 2030-04-16" in text
    assert "Decisions to make" in text
    assert "examples/meeting-transcript.md" in text
    assert "agents/demo/memory/commitments.jsonl" in text


def test_meeting_prep_selects_event_by_id() -> None:
    brief = build_meeting_prep(Path.cwd(), event_id="evt_demo_001")

    assert brief.event["title"] == "Riverbend launch review"


def test_meeting_prep_rejects_unknown_event_id() -> None:
    with pytest.raises(ValueError, match="event not found"):
        build_meeting_prep(Path.cwd(), event_id="missing")
