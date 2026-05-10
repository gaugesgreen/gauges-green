# Contributing

Keep examples synthetic. Do not add real contacts, client names, message bodies,
calendar exports, credentials, screenshots with private text, or private local
paths.

The publication boundary is permanent: real memory, contacts, transcripts,
inbox/calendar/message exports, client examples, production configs, credentials,
IDs, tokens, local paths, and private names never belong in this repository.
See `PUBLICATION_POLICY.md`.

Before opening a pull request:

```bash
.venv/bin/python -m pytest
./scripts/preflight.sh
```

Prefer small changes with focused tests. If a fixture needs to resemble a real
workflow, recreate it from scratch with invented names, dates, IDs, and domains.
Do not sanitize copied private files with search-and-replace.
