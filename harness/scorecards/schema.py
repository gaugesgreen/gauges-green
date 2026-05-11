from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

from harness.scorecards.grade import grade_to_score

SCHEMA_VERSION = 1


@dataclass(frozen=True)
class PillarScore:
    key: str
    grade: str
    evidence: str

    def to_dict(self) -> dict[str, object]:
        return {
            "key": self.key,
            "grade": self.grade,
            "numeric": grade_to_score(self.grade),
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class ScorecardRow:
    agent: str
    as_of: str
    overall_grade: str
    pillars: tuple[PillarScore, ...]
    schema_version: int = SCHEMA_VERSION

    def to_dict(self) -> dict[str, object]:
        row = asdict(self)
        row["overall_numeric"] = grade_to_score(self.overall_grade)
        row["pillars"] = [pillar.to_dict() for pillar in self.pillars]
        return row

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


def load_history(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(f"{path}:{line_number} unsupported schema_version")
        rows.append(row)
    return rows


def demo_row() -> ScorecardRow:
    return ScorecardRow(
        agent="demo",
        as_of=date(2030, 4, 15).isoformat(),
        overall_grade="B+",
        pillars=(
            PillarScore(
                key="reliability",
                grade="A-",
                evidence="Boot manifest compiled from seven synthetic sources without missing required files.",
            ),
            PillarScore(
                key="governance",
                grade="B+",
                evidence="Gate stack blocked unsupported claims in the bad-output fixture.",
            ),
            PillarScore(
                key="documentation",
                grade="B",
                evidence="README and docs explain the public extraction boundary.",
            ),
        ),
    )
