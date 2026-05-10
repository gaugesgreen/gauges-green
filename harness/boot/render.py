from __future__ import annotations

from dataclasses import dataclass

from harness.boot.manifest import BootManifest


@dataclass(frozen=True)
class CompiledSource:
    label: str
    relative_path: str
    content: str
    truncated: bool = False


@dataclass(frozen=True)
class BootPayload:
    manifest: BootManifest
    sources: tuple[CompiledSource, ...]


def render_payload(payload: BootPayload) -> str:
    lines: list[str] = [
        f"# Boot Payload: {payload.manifest.agent}",
        "",
        payload.manifest.summary,
        "",
        "## Loaded Sources",
    ]

    for source in payload.sources:
        suffix = " (truncated)" if source.truncated else ""
        lines.extend(
            [
                "",
                f"### {source.label}{suffix}",
                "",
                f"Source: `{source.relative_path}`",
                "",
                source.content.strip(),
            ]
        )

    lines.extend(
        [
            "",
            "## Opening Brief",
            "",
            "The demo agent is ready with synthetic identity, operating rules, tool contracts,",
            "working context, contacts, and commitments. It should cite loaded context when",
            "making assertions and route unsupported claims through the gate stack.",
            "",
        ]
    )
    return "\n".join(lines)
