# Gauges Green

[![CI](https://github.com/gaugesgreen/gauges-green/actions/workflows/ci.yml/badge.svg)](https://github.com/gaugesgreen/gauges-green/actions/workflows/ci.yml)

Production-shaped agent operating harness extracted into a safe public demo.

This is the public extraction of the production harness we run inside Gauges
Green. The architecture, gates, scorecards, and agent patterns are real. The
private client data, live credentials, and personal memory stores have been
replaced with synthetic examples.

This is the production shape, extracted into a public repo you can run safely.

## See It Work

```bash
./setup
./gg demo
```

Then run the pieces directly:

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

## Highlights

- `gg` launcher
- boot manifest compiler
- synthetic demo agent
- gate stack examples
- scorecard schema and grade arithmetic
- Claude Code hook examples
- docs for Pulse, Critique, Pluma, Scribe, briefs, avisos, and evals

## Demo Agent

The `agents/demo` agent loads identity from `SOUL.md`, operating rules from
`AGENTS.md`, tool contracts from `TOOLS.md`, and synthetic context from its boot
manifest. The compiled boot payload is printed to stdout and can also be used as
the first-message context for an agent session.

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
.venv/bin/python -m harness.boot --agent demo
.venv/bin/python -m harness.gates examples/agent-output-good.md
.venv/bin/python -m harness.gates examples/agent-output-bad.md || true
./scripts/preflight.sh
```

## License

Code is MIT licensed. Documentation and examples are CC-BY-4.0 licensed.
