from __future__ import annotations

import argparse
from pathlib import Path

from harness.boot.compiler import BootCompiler
from harness.demo.workflow import render_report, run_demo
from harness.gates.runner import run_gates
from harness.scorecards.schema import demo_row


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gg", description="Gauges Green harness launcher.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo_parser = subparsers.add_parser("demo", help="run the synthetic demo")
    demo_parser.add_argument("--agent", default="demo")

    subparsers.add_parser("run-demo", help="run the guided synthetic walkthrough")

    boot_parser = subparsers.add_parser("boot", help="compile a boot payload")
    boot_parser.add_argument("--agent", default="demo")

    gates_parser = subparsers.add_parser("gates", help="run gates against a file")
    gates_parser.add_argument("path", type=Path)

    scorecard_parser = subparsers.add_parser("scorecard", help="print the demo scorecard row")
    scorecard_parser.set_defaults(scorecard=True)

    args = parser.parse_args(argv)
    if args.command == "demo":
        return _demo(args.agent)
    if args.command == "run-demo":
        report = run_demo(Path.cwd())
        print(render_report(report), end="")
        return 0 if report.ok else 1
    if args.command == "boot":
        print(BootCompiler().render(args.agent), end="")
        return 0
    if args.command == "gates":
        result = run_gates(args.path.read_text())
        if result.ok:
            print(f"PASS {args.path}")
            return 0
        print(f"FAIL {args.path}")
        for finding in result.findings:
            location = f":{finding.line}" if finding.line is not None else ""
            print(f"- {finding.gate}{location}: {finding.message}")
        return 1
    if args.command == "scorecard":
        print(demo_row().to_json())
        return 0
    parser.error("unknown command")
    return 2


def _demo(agent: str) -> int:
    compiler = BootCompiler()
    payload = compiler.render(agent)
    bad_output = Path("examples/agent-output-bad.md").read_text()
    gate_result = run_gates(bad_output)

    print("== Boot ==")
    print(payload.split("## Opening Brief", 1)[0].rstrip())
    print()
    print("== Gate Check ==")
    if gate_result.ok:
        print("unexpected pass for bad-output fixture")
        return 1
    for finding in gate_result.findings:
        location = f":{finding.line}" if finding.line is not None else ""
        print(f"- {finding.gate}{location}: {finding.message}")
    print()
    print("== Scorecard ==")
    print(demo_row().to_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
