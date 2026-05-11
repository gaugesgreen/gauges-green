from pathlib import Path

from harness.demo.workflow import render_report, run_demo


def test_run_demo_blocks_bad_output_and_passes_good_output() -> None:
    report = run_demo(Path.cwd())

    assert report.ok
    assert report.compiled_source_count >= 6
    assert not report.bad_gate_result.ok
    assert report.good_gate_result.ok


def test_run_demo_report_is_screenshot_readable() -> None:
    text = render_report(run_demo(Path.cwd()))

    assert "Gauges Green Harness Demo" in text
    assert "Bad draft gate result" in text
    assert "Corrected draft gate result" in text
    assert "demo passed" in text
