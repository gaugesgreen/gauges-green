# Boot Manifest

A boot manifest names the agent and lists source files to compile into a boot
payload. Sources are resolved relative to the manifest file.

```json
{
  "agent": "demo",
  "summary": "Synthetic demo boot manifest.",
  "sources": [{"label": "Identity", "path": "SOUL.md"}]
}
```
