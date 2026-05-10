# Getting Started

```bash
./setup
./gg demo
.venv/bin/python -m harness.boot --agent demo
.venv/bin/python -m harness.gates examples/agent-output-bad.md || true
.venv/bin/python -m pytest
```

The bad-output gate command should fail visibly.
