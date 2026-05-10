# Gates

The v0.1 gate stack is intentionally small:

- assertion auditor
- drift linter
- date arithmetic checker
- recipient-language checker

Run it with:

```bash
.venv/bin/python -m harness.gates examples/agent-output-good.md
.venv/bin/python -m harness.gates examples/agent-output-bad.md || true
```
