#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from harness.gates.drift_linter import lint_drift


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: handler.py OUTPUT_PATH", file=sys.stderr)
        return 2
    findings = lint_drift(Path(sys.argv[1]).read_text())
    for finding in findings:
        print(f"{finding.gate}:{finding.line}: {finding.message}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
