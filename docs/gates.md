# Gates

The v0.1 gate stack is intentionally small:

- assertion auditor
- drift linter
- date arithmetic checker
- recipient-language checker

Run it with:

```bash
python3 -m harness.gates examples/agent-output-good.md
python3 -m harness.gates examples/agent-output-bad.md
```
