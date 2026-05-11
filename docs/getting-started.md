# Getting Started

```bash
./setup
./gg run-demo
.venv/bin/python -m pytest
.venv/bin/python -m harness.boot --agent demo
.venv/bin/python -m harness.gates examples/agent-output-bad.md || true
```

The bad-output gate command should fail visibly.
