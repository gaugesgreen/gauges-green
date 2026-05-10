from pathlib import Path

from harness.gates.runner import run_gates


def test_good_output_passes() -> None:
    result = run_gates(Path("examples/agent-output-good.md").read_text())
    assert result.ok


def test_bad_output_fails_multiple_gates() -> None:
    result = run_gates(Path("examples/agent-output-bad.md").read_text())
    assert not result.ok
    gates = {finding.gate for finding in result.findings}
    assert "assertion-auditor" in gates
    assert "drift-linter" in gates
    assert "time-arithmetic" in gates
