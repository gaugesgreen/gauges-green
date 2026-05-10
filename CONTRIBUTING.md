# Contributing

Keep examples synthetic. Do not add real contacts, client names, message bodies,
calendar exports, credentials, screenshots with private text, or private local
paths.

Before opening a pull request:

```bash
python3 -m pytest
./scripts/preflight.sh
```

Prefer small changes with focused tests. If a fixture needs to resemble a real
workflow, recreate it from scratch with invented names, dates, IDs, and domains.
