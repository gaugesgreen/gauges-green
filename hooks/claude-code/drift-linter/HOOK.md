# Drift Linter Hook

Example hook contract:

```bash
python3 hooks/claude-code/drift-linter/handler.py path/to/output.md
```

The handler exits non-zero when public positioning drifts toward unsafe claims.
