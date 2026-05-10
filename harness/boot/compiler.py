from __future__ import annotations

import argparse
from pathlib import Path

from harness.boot.manifest import BootManifest, ManifestError, load_manifest
from harness.boot.render import BootPayload, CompiledSource, render_payload


class BootCompiler:
    def __init__(self, repo_root: Path | None = None) -> None:
        self.repo_root = repo_root or Path.cwd()

    def compile(self, agent: str) -> BootPayload:
        manifest_path = self.repo_root / "agents" / agent / "boot-manifest.json"
        if not manifest_path.exists():
            raise ManifestError(f"unknown agent or missing manifest: {agent}")
        manifest = load_manifest(manifest_path)
        return BootPayload(manifest=manifest, sources=self._compile_sources(manifest))

    def render(self, agent: str) -> str:
        return render_payload(self.compile(agent))

    def _compile_sources(self, manifest: BootManifest) -> tuple[CompiledSource, ...]:
        compiled: list[CompiledSource] = []
        for source in manifest.sources:
            if not source.path.exists():
                if source.required:
                    raise ManifestError(f"required source missing: {source.path}")
                continue
            content = source.path.read_text()
            truncated = False
            if source.max_chars is not None and len(content) > source.max_chars:
                content = content[: source.max_chars].rstrip() + "\n\n[truncated]"
                truncated = True
            compiled.append(
                CompiledSource(
                    label=source.label,
                    relative_path=str(source.path.relative_to(self.repo_root)),
                    content=content,
                    truncated=truncated,
                )
            )
        return tuple(compiled)


def compile_agent(agent: str, repo_root: Path | None = None) -> BootPayload:
    return BootCompiler(repo_root=repo_root).compile(agent)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile a synthetic agent boot payload.")
    parser.add_argument("--agent", default="demo", help="agent directory under agents/")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    args = parser.parse_args(argv)

    try:
        print(BootCompiler(repo_root=args.root).render(args.agent), end="")
    except ManifestError as exc:
        parser.error(str(exc))
    return 0
