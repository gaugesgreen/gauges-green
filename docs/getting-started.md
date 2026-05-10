# Getting Started

```bash
./setup
./gg demo
python3 -m harness.boot --agent demo
python3 -m harness.gates examples/agent-output-bad.md
python3 -m pytest
```

The bad-output gate command should fail visibly.
