# Architecture

The public harness has four small layers:

1. Agent files define identity, operating rules, tools, and memory-like context.
2. Boot manifests declare which files become the session payload.
3. Gates inspect generated text before it is treated as sendable.
4. Scorecards preserve evaluation evidence in a stable JSONL shape.

```text
agent files -> boot compiler -> agent output -> gates -> scorecard evidence
```
