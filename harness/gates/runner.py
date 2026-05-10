from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from harness.gates.assertion_auditor import audit_assertions
from harness.gates.drift_linter import lint_drift
from harness.gates.recipient_language import lint_recipient_language
from harness.gates.time_arithmetic import lint_time_arithmetic


@dataclass(frozen=True)
class GateFinding:
    gate: str
    message: str
    line: int | None = None


@dataclass(frozen=True)
class GateResult:
    findings: tuple[GateFinding, ...]

    @property
    def ok(self) -> bool:
        return not self.findings


def run_gates(text: str) -> GateResult:
    findings: list[GateFinding] = []
    findings.extend(audit_assertions(text))
    findings.extend(lint_drift(text))
    findings.extend(lint_time_arithmetic(text))
    findings.extend(lint_recipient_language(text))
    return GateResult(findings=tuple(findings))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run public harness gates against output text.")
    parser.add_argument("path", type=Path, help="markdown or text file to check")
    args = parser.parse_args(argv)

    text = args.path.read_text()
    result = run_gates(text)
    if result.ok:
        print(f"PASS {args.path}")
        return 0

    print(f"FAIL {args.path}")
    for finding in result.findings:
        location = f":{finding.line}" if finding.line is not None else ""
        print(f"- {finding.gate}{location}: {finding.message}")
    return 1
