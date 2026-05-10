# Gauges Green Harness

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
python3 -m harness.boot --agent demo
python3 -m harness.gates examples/agent-output-bad.md
python3 -m pytest
```

The bad-output gate command is expected to exit non-zero because it catches
unsupported claims in the fixture.

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

## Development

```bash
python3 -m pytest
python3 -m harness.boot --agent demo
python3 -m harness.gates examples/agent-output-good.md
python3 -m harness.gates examples/agent-output-bad.md
./scripts/preflight.sh
```

## License

Code is MIT licensed. Documentation and examples are CC-BY-4.0 licensed.
