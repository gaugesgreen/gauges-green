# Meeting Prep

Status: v0 synthetic demo

## Purpose

Show how the harness turns scattered operating context into a pre-meeting brief.

The v0 feature is deliberately small and public-safe. It reads only committed
synthetic fixtures:

- `examples/calendar.json`
- `examples/meeting-transcript.md`
- `agents/demo/memory/commitments.jsonl`

## Run It

```bash
./gg meeting-prep
```

## Output Shape

The brief includes:

1. Meeting title, time, and attendees.
2. What happened last time.
3. Open commitments.
4. Decisions to make.
5. Source paths.

## Boundary

This demo must not read private calendars, mailboxes, transcripts, client docs,
or production memory stores. Real integrations belong behind explicit
publication and privacy gates.
