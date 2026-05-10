from __future__ import annotations

import calendar
import re
from datetime import date

from harness.gates.runner_types import Finding

DATE_DOW_RE = re.compile(
    r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+"
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
    r"(\d{1,2}),\s+(20\d{2})\b"
)


def lint_time_arithmetic(text: str) -> list[Finding]:
    findings: list[Finding] = []
    month_numbers = {name: index for index, name in enumerate(calendar.month_name) if name}
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in DATE_DOW_RE.finditer(line):
            claimed_dow, month_name, day_text, year_text = match.groups()
            actual = date(int(year_text), month_numbers[month_name], int(day_text)).strftime("%A")
            if actual != claimed_dow:
                findings.append(
                    Finding(
                        gate="time-arithmetic",
                        line=line_number,
                        message=f"{match.group(0)!r} is a {actual}, not a {claimed_dow}",
                    )
                )
    return findings
