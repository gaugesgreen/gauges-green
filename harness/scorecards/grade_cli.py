from __future__ import annotations

from harness.scorecards.schema import demo_row


def main() -> int:
    print(demo_row().to_json())
    return 0
