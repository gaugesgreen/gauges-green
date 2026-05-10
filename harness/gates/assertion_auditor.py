from __future__ import annotations

import re

from harness.gates.runner_types import Finding

ABSOLUTE_CLAIM_RE = re.compile(
    r"\b(guaranteed|definitely|always|never|confirmed|the client said|the customer said)\b",
    re.IGNORECASE,
)
EVIDENCE_RE = re.compile(r"\b(evidence|source|according to|fixture|calendar|inbox|transcript)\b", re.IGNORECASE)


def audit_assertions(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = ABSOLUTE_CLAIM_RE.search(line)
        if not match:
            continue
        if EVIDENCE_RE.search(line):
            continue
        findings.append(
            Finding(
                gate="assertion-auditor",
                line=line_number,
                message=f"unsupported high-confidence claim: {match.group(0)!r}",
            )
        )
    return findings
