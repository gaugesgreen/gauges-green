# Gauges Green

[![CI](https://github.com/gaugesgreen/gauges-green/actions/workflows/ci.yml/badge.svg)](https://github.com/gaugesgreen/gauges-green/actions/workflows/ci.yml)

A public-safe demo of the AI operating harness Gauges Green uses to run a
senior-operator practice.

![Compiled context flow](https://www.gaugesgreen.com/harness/story-compiled-context.svg)

Independent client work creates a second job around the work: context, meeting
prep, follow-ups, proposals, billing, collections, pipeline, and quality control.

This repo shows the harness shape behind that work. It compiles context before
an agent starts, gates output before it leaves, and records scorecard evidence
over time.

The architecture is real. The data is synthetic.

## Why This Exists

Most agent projects start with a blank chat window and a pile of prompts. That
works until the agent needs to remember the business, respect boundaries, verify
claims, route work, and show its own performance over time.

Gauges Green starts from the opposite direction. The agent is only one part of
the operating system. The harness supplies context, tools, gates, scorecards,
and publication boundaries around it.

## See It Work

```bash
./setup
./gg run-demo
```

That prints a compact walkthrough: fixture load, boot compilation, bad draft
blocked by gates, corrected draft passed, and a scorecard row.

To see the meeting prep feature:

```bash
./gg meeting-prep
```

That prints a synthetic pre-meeting brief from the demo calendar, prior meeting
transcript, and open commitments. It is public-safe: the feature uses only
fixtures committed under `examples/` and `agents/demo/memory/`.

You can also run the pieces directly:

```bash
.venv/bin/python -m harness.boot --agent demo
.venv/bin/python -m pytest
```

To see a gate catch bad output:

```bash
.venv/bin/python -m harness.gates examples/agent-output-bad.md || true
```

That command is expected to exit non-zero because it catches unsupported claims
in the fixture.

## What Is In The Harness

- `gg` launcher
- Boot manifest compiler
- Meeting prep brief from synthetic calendar, transcript, and commitments
- Synthetic demo agent
- Gate stack examples
- Scorecard schema and grade arithmetic
- Claude Code hook examples
- Docs for Pulse, Critique, Pluma, Scribe, briefs, avisos, and evals

## Core Loop

1. Compile context before the agent starts.
2. Run the agent inside a bounded domain.
3. Check the work before it leaves.
4. Write durable state back to memory.
5. Grade the function with evidence.

The demo agent loads identity from `SOUL.md`, operating rules from `AGENTS.md`,
tool contracts from `TOOLS.md`, and synthetic context from its boot manifest.
The compiled boot payload is printed to stdout and can also be used as the
first-message context for an agent session.

## How This Relates To GStack And OpenClaw

GStack gives coding agents structured roles and workflows. OpenClaw gives
personal agents local surfaces and message routing. Gauges Green is the
operator-work layer: client context in, governed work out, evidence attached.

## What Is In This Repo

- Synthetic data fixtures under `examples/`
- A small Python boot compiler under `harness/boot/`
- Public-safe gate examples under `harness/gates/`
- Scorecard schema and grading utilities under `harness/scorecards/`
- Minimal CLI entrypoints under `harness/cli/`

## What Is Not In This Repo

- Private memory stores
- Real contacts, messages, calendars, proposals, or client records
- Live credentials or communication configuration
- Private source repository history

The publication boundary is permanent. See `PUBLICATION_POLICY.md`.

## Development

```bash
.venv/bin/python -m pytest
.venv/bin/python -m harness.cli.gg run-demo
.venv/bin/python -m harness.boot --agent demo
.venv/bin/python -m harness.gates examples/agent-output-good.md
.venv/bin/python -m harness.gates examples/agent-output-bad.md || true
./scripts/preflight.sh
```

## Learn More

- [Harness overview](https://www.gaugesgreen.com/harness)
- [Build log](https://www.gaugesgreen.com/log)

## License

Code is MIT licensed. Documentation and examples are CC-BY-4.0 licensed.
