# Publication Policy

Gauges Green public repositories must never include real private operating data.

This is a permanent rule. It applies even when data seems harmless, old,
partially redacted, already known to a recipient, or useful as an example.

## Never Publish

- real memory
- real contacts
- real transcripts
- real inbox, calendar, CRM, chat, or message exports
- real client examples
- real proposals, scorecards, or operating histories
- production configs
- credentials, API keys, OAuth tokens, cookies, session IDs, webhook secrets, or
  refresh tokens
- real message IDs, thread IDs, document IDs, chat IDs, calendar IDs, phone
  numbers, addresses, private names, or local machine paths
- screenshots or recordings containing private text, metadata, account names, or
  system notifications

## Allowed Public Material

- synthetic fixtures created from scratch
- abstracted architecture
- reusable code primitives
- templates
- docs explaining patterns
- tests and evals against invented data

## Synthetic Fixture Rules

Public fixtures must use:

- `example.com` email addresses
- `+1555010xxxx` phone-style values
- fake dates in 2030 or later
- invented names and companies
- IDs prefixed with obvious synthetic markers such as `demo_`, `evt_demo_`,
  `msg_demo_`, `thr_demo_`, or `commit-demo-`

Do not sanitize copied private files with search-and-replace. Recreate fixtures
from scratch.

## Review Requirements

Before publishing or merging:

```bash
python3 -m pytest
./scripts/preflight.sh
```

Any broad privacy scan hit must be classified as synthetic, policy text, test
logic, or a blocker. Blockers are removed, not redacted in place.
