# `gg run-demo` Spec

Status: Planned for v0.1.1

## Purpose

Give a first-time visitor one command that demonstrates the Gauges Green
operating loop in under 60 seconds:

```bash
./gg run-demo
```

The command should make the repo feel like a working harness, not a collection
of parts.

## Non-Negotiable Boundary

The workflow must use only synthetic fixtures already in the repo or new
fixtures created from scratch under the publication policy. It must never call
private mailboxes, calendars, memory stores, transcripts, production configs, or
external services.

## User Experience

`./gg run-demo` should print a compact terminal report with these sections:

1. Fixture load summary
2. Boot payload compilation summary
3. Bad draft gate result
4. Corrected draft gate result
5. Scorecard row
6. Final summary

The report should be readable in a LinkedIn screenshot and useful in a terminal.
Avoid dumping the full boot payload by default; include counts, filenames, and
short excerpts.

## Workflow

1. Load synthetic fixtures:
   - `examples/inbox.jsonl`
   - `examples/calendar.json`
   - `examples/contacts.json`
   - `examples/meeting-transcript.md`
   - `examples/agent-output-bad.md`
   - `examples/agent-output-good.md`
2. Compile the demo boot payload with the existing boot compiler.
3. Run gates against `agent-output-bad.md`; expect failure.
4. Run gates against `agent-output-good.md`; expect pass.
5. Build the demo scorecard row with existing scorecard utilities.
6. Print the report and exit `0` only when the expected fail/pass pattern holds.

## Proposed Implementation

Add:

```text
harness/demo/
  __init__.py
  workflow.py
tests/
  test_run_demo.py
```

Extend:

```text
harness/cli/gg.py
```

with a `run-demo` subcommand.

`workflow.py` should expose a testable function:

```python
def run_demo(repo_root: Path) -> DemoReport:
    ...
```

The CLI should render `DemoReport` to text and return its exit code.

## Acceptance Criteria

1. `./setup` succeeds from a fresh clone.
2. `./gg run-demo` exits `0`.
3. The report shows bad output blocked and good output passed.
4. `python3 -m pytest` passes.
5. `./scripts/preflight.sh` passes.
6. No network calls are made.
7. No private-data policy exceptions are introduced.
8. README uses `./gg run-demo` as the primary demo command.

## Nice-To-Have

- `./gg run-demo --json` for machine-readable output.
- `./gg run-demo --show-boot` to print the full boot payload.
- `examples/demo-report.md` generated from a committed sample run.
