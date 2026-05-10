from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    gate: str
    message: str
    line: int | None = None
