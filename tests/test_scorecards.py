from pathlib import Path

from harness.scorecards.grade import delta_steps, grade_to_score, score_to_grade
from harness.scorecards.schema import demo_row, load_history


def test_grade_arithmetic() -> None:
    assert grade_to_score("B+") == 3.3
    assert score_to_grade(3.31) == "B+"
    assert delta_steps("B", "A-") == "+2"


def test_demo_scorecard_schema_matches_history_fixture() -> None:
    row = demo_row().to_dict()
    assert row["schema_version"] == 1
    assert row["overall_grade"] == "B+"

    history = load_history(Path("examples/scorecard-history.jsonl"))
    assert history[0]["schema_version"] == 1
    assert history[0]["agent"] == "demo"
