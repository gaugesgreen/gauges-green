from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ManifestError(ValueError):
    """Raised when a boot manifest is invalid."""


@dataclass(frozen=True)
class ManifestSource:
    label: str
    path: Path
    required: bool = True
    max_chars: int | None = None


@dataclass(frozen=True)
class BootManifest:
    agent: str
    summary: str
    sources: tuple[ManifestSource, ...]


def load_manifest(path: Path) -> BootManifest:
    raw: dict[str, Any] = json.loads(path.read_text())
    agent = _required_str(raw, "agent")
    summary = _required_str(raw, "summary")
    sources: list[ManifestSource] = []

    for index, row in enumerate(raw.get("sources", []), start=1):
        if not isinstance(row, dict):
            raise ManifestError(f"source #{index} must be an object")
        label = _required_str(row, "label")
        source_path = _required_str(row, "path")
        required = bool(row.get("required", True))
        max_chars = row.get("max_chars")
        if max_chars is not None and (not isinstance(max_chars, int) or max_chars <= 0):
            raise ManifestError(f"source #{index} max_chars must be a positive integer")
        sources.append(
            ManifestSource(
                label=label,
                path=(path.parent / source_path).resolve(),
                required=required,
                max_chars=max_chars,
            )
        )

    if not sources:
        raise ManifestError("manifest must include at least one source")

    return BootManifest(agent=agent, summary=summary, sources=tuple(sources))


def _required_str(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{key} must be a non-empty string")
    return value.strip()
