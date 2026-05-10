# Publishing Notes

Before public push:

```bash
.venv/bin/python -m pytest
./scripts/preflight.sh
git log --oneline --all
```

Do not publish if the repo contains private source history, live credentials,
real contacts, real message bodies, private memory files, or copied production
fixtures.

## v0.1 Release Review

Reviewed on 2026-05-10 before first public push:

- `examples/` contains synthetic names, dates, IDs, companies, and `example.com`
  addresses, except `agent-output-bad.md`, which intentionally includes a
  non-example invalid domain so the drift gate has a visible failure.
- `agents/demo/memory/` contains recreated synthetic context only.
- README positioning says this is a public extraction and does not claim exact
  live production contents.
- Local Git history was initialized fresh in this repository.
