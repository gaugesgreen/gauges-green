from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from harness.boot.compiler import BootCompiler
from harness.gates.runner import GateResult, run_gates
from harness.scorecards.schema import ScorecardRow, demo_row


@dataclass(frozen=True)
class DemoReport:
    repo_root: Path
    fixture_paths: tuple[Path, ...]
    compiled_source_count: int
    compiled_char_count: int
    boot_excerpt: str
    bad_gate_result: GateResult
    good_gate_result: GateResult
    scorecard_row: ScorecardRow

    @property
    def ok(self) -> bool:
        return not self.bad_gate_result.ok and self.good_gate_result.ok


FIXTURE_PATHS = (
    Path("examples/inbox.jsonl"),
    Path("examples/calendar.json"),
    Path("examples/contacts.json"),
    Path("examples/meeting-transcript.md"),
    Path("examples/agent-output-bad.md"),
    Path("examples/agent-output-good.md"),
)


def run_demo(repo_root: Path) -> DemoReport:
    compiler = BootCompiler(repo_root=repo_root)
    payload = compiler.compile("demo")
    rendered = compiler.render("demo")
    bad_output = (repo_root / "examples/agent-output-bad.md").read_text()
    good_output = (repo_root / "examples/agent-output-good.md").read_text()

    return DemoReport(
        repo_root=repo_root,
        fixture_paths=FIXTURE_PATHS,
        compiled_source_count=len(payload.sources),
        compiled_char_count=len(rendered),
        boot_excerpt=_excerpt(rendered),
        bad_gate_result=run_gates(bad_output),
        good_gate_result=run_gates(good_output),
        scorecard_row=demo_row(),
    )


def render_report(report: DemoReport) -> str:
    lines: list[str] = []
    lines.append("Gauges Green Harness Demo")
    lines.append("")
    lines.append("1. Fixture load summary")
    for path in report.fixture_paths:
        status = "loaded" if (report.repo_root / path).exists() else "missing"
        lines.append(f"   - {path}: {status}")
    lines.append("")
    lines.append("2. Boot payload compilation")
    lines.append(f"   - compiled sources: {report.compiled_source_count}")
    lines.append(f"   - payload chars: {report.compiled_char_count}")
    lines.append("   - excerpt:")
    for line in report.boot_excerpt.splitlines():
        lines.append(f"     {line}")
    lines.append("")
    lines.append("3. Bad draft gate result")
    if report.bad_gate_result.ok:
        lines.append("   - unexpected pass")
    else:
        lines.append(f"   - blocked with {len(report.bad_gate_result.findings)} finding(s)")
        for finding in report.bad_gate_result.findings:
            location = f":{finding.line}" if finding.line is not None else ""
            lines.append(f"   - {finding.gate}{location}: {finding.message}")
    lines.append("")
    lines.append("4. Corrected draft gate result")
    lines.append("   - pass" if report.good_gate_result.ok else "   - unexpected fail")
    for finding in report.good_gate_result.findings:
        location = f":{finding.line}" if finding.line is not None else ""
        lines.append(f"   - {finding.gate}{location}: {finding.message}")
    lines.append("")
    lines.append("5. Scorecard row")
    row = report.scorecard_row.to_dict()
    lines.append(
        f"   - {row['agent']} {row['as_of']}: {row['overall_grade']} "
        f"({row['overall_numeric']})"
    )
    for pillar in row["pillars"]:
        lines.append(f"   - {pillar['key']}: {pillar['grade']} - {pillar['evidence']}")
    lines.append("")
    lines.append("6. Final summary")
    if report.ok:
        lines.append("   - demo passed: bad output blocked, corrected output passed")
    else:
        lines.append("   - demo failed: expected bad output to block and corrected output to pass")
    return "\n".join(lines) + "\n"


def _excerpt(text: str, max_lines: int = 8) -> str:
    return "\n".join(text.splitlines()[:max_lines])
