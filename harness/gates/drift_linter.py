from __future__ import annotations

import re

from harness.gates.runner_types import Finding

EXACT_PRODUCTION_CLAIM_RE = re.compile(
    r"\b(actual production system|exact live production system|real client data|live credentials)\b",
    re.IGNORECASE,
)
NON_EXAMPLE_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@(?!example\.com\b)[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def lint_drift(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if EXACT_PRODUCTION_CLAIM_RE.search(line):
            findings.append(
                Finding(
                    gate="drift-linter",
                    line=line_number,
                    message="public copy must describe an extracted production shape, not exact live production contents",
                )
            )
        if NON_EXAMPLE_EMAIL_RE.search(line):
            findings.append(
                Finding(
                    gate="drift-linter",
                    line=line_number,
                    message="fixture email domains must use example.com",
                )
            )
    return findings
