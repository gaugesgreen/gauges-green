from __future__ import annotations

GRADE_ORDER: tuple[str, ...] = (
    "F",
    "D-",
    "D",
    "D+",
    "C-",
    "C",
    "C+",
    "B-",
    "B",
    "B+",
    "A-",
    "A",
    "A+",
)

GRADE_TO_SCORE: dict[str, float] = {
    "A+": 4.3,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "D-": 0.7,
    "F": 0.0,
}

GRADE_TO_STEP = {grade: index for index, grade in enumerate(GRADE_ORDER)}


class GradeError(ValueError):
    """Raised for unknown grade values."""


def clean_grade(raw: str) -> str:
    value = str(raw).strip().replace("**", "").replace("\u2212", "-")
    if not value:
        raise GradeError("empty grade")
    value = value[0].upper() + value[1:]
    if value not in GRADE_TO_SCORE:
        raise GradeError(f"unknown grade: {raw!r}")
    return value


def grade_to_score(grade: str) -> float:
    return GRADE_TO_SCORE[clean_grade(grade)]


def score_to_grade(score: float) -> str:
    best = "F"
    best_distance = float("inf")
    for grade in GRADE_ORDER:
        distance = abs(float(score) - GRADE_TO_SCORE[grade])
        if distance <= best_distance:
            best = grade
            best_distance = distance
    return best


def delta_steps(old: str | None, new: str) -> str | None:
    if old is None:
        return None
    diff = GRADE_TO_STEP[clean_grade(new)] - GRADE_TO_STEP[clean_grade(old)]
    if diff > 0:
        return f"+{diff}"
    return str(diff)
