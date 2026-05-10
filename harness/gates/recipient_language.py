from __future__ import annotations

import re

from harness.gates.runner_types import Finding

MIXED_LANGUAGE_RE = re.compile(r"\b(hola|gracias|por favor)\b.*\b(please|thanks|hello)\b", re.IGNORECASE)


def lint_recipient_language(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if MIXED_LANGUAGE_RE.search(line):
            findings.append(
                Finding(
                    gate="recipient-language",
                    line=line_number,
                    message="mixed recipient language needs an explicit reason or rewrite",
                )
            )
    return findings
