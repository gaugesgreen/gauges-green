from pathlib import Path

from harness.boot.compiler import BootCompiler


def test_demo_boot_payload_loads_identity_and_context() -> None:
    payload = BootCompiler(repo_root=Path.cwd()).render("demo")
    assert "# Boot Payload: demo" in payload
    assert "Demo Agent Identity" in payload
    assert "Working Context" in payload
    assert "Opening Brief" in payload
