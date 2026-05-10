#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
if [ -z "${PYTHON:-}" ]; then
  if [ -x ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
  else
    PYTHON="python3"
  fi
fi

echo "== tests =="
"$PYTHON" -m pytest

echo "== smoke =="
"$PYTHON" -m harness.boot --agent demo >/tmp/gg-harness-boot-smoke.md
if "$PYTHON" -m harness.gates examples/agent-output-bad.md >/tmp/gg-harness-bad-gate.txt 2>&1; then
  echo "expected bad fixture to fail gates" >&2
  exit 1
fi

echo "== hard privacy patterns =="
blocked_paths="$(find . -not -path './.git/*' -not -path './.venv/*' -not -path './*.egg-info/*' \( \
  -name '.env' -o \
  \( -name '.env.*' ! -name '.env.example' \) -o \
  -name 'CONTACTS.md' -o \
  -name 'MEMORY.md' -o \
  -name 'agents_archived' -o \
  -name 'drafts' -o \
  -name 'trips' -o \
  -name 'Family_Recipes.md' -o \
  -name '*transcript*real*' -o \
  -name '*contacts*real*' -o \
  -name '*memory*real*' -o \
  -path './memory' -o \
  -path './memory/*' -o \
  -path './gauges-green/proposals' -o \
  -path './gauges-green/proposals/*' \
\) -print)"
if [ -n "$blocked_paths" ]; then
  echo "$blocked_paths"
  echo "blocked private path found" >&2
  exit 1
fi

if rg -n --hidden --glob '!.git/**' --glob '!.venv/**' --glob '!*.egg-info/**' --glob '!scripts/preflight.sh' \
  '(/Users/eberhard/clawd|/Users/eberhard/Obsidian-Vault|eberhard@|CONTACTS\.md|MEMORY\.md|memory\.bak|agents_archived|config/.*(token|credential|whatsapp|gmail)|gauges-green/proposals|voice-samples\.jsonl|refresh_token|client_secret|xox[baprs]-|gh[pousr]_[A-Za-z0-9_]+)' .; then
  echo "hard privacy pattern found" >&2
  exit 1
fi

echo "== broad review scan =="
rg -n -i --hidden --glob '!.git/**' --glob '!.venv/**' --glob '!*.egg-info/**' \
  'token|secret|password|oauth|bearer|api[_-]?key|client_secret|refresh_token|telegram|whatsapp|gmail|supabase|monark|family|sonia|contact|phone|email' . || true

echo "== large files =="
large_files="$(find . -type f -not -path './.git/*' -not -path './.venv/*' -not -path './*.egg-info/*' -size +1M -print)"
if [ -n "$large_files" ]; then
  echo "$large_files"
  echo "large files require review" >&2
  exit 1
fi

echo "== images =="
find . -type f -not -path './.venv/*' -not -path './*.egg-info/*' \( -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' \) -print

if command -v gitleaks >/dev/null 2>&1; then
  echo "== gitleaks =="
  gitleaks detect --no-git --source .
else
  echo "gitleaks not installed; skipped"
fi

echo "== git history =="
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git log --oneline --all || true
  git status --short
else
  echo "not a git repository yet"
fi

echo "preflight passed"
