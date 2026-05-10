import json
import re
from pathlib import Path


PUBLIC_FIXTURE_ROOTS = (Path("examples"), Path("agents/demo"))
ALLOWED_EMAIL_DOMAINS = {"example.com"}
ALLOWED_NON_EXAMPLE_EMAILS = {"riley.chen@northstar.invalid"}
ALLOWED_NAMES = {
    "Avery Stone",
    "Morgan Vale",
    "Riley Chen",
    "Northstar Demo Labs",
    "Riverbend Example",
    "Riverbend Example Co",
    "Demo Harness Agent",
    "Gauges Green",
}
FORBIDDEN_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"/Users/eberhard/",
        r"\brefresh" + r"_token\b",
        r"\bclient" + r"_secret\b",
        r"\bapi[_-]?key\b",
        r"\boauth\b",
        r"\bbearer\s+[A-Za-z0-9._-]+",
        r"\bgh[pousr]_[A-Za-z0-9_]+",
        r"\bxox[baprs]-[A-Za-z0-9-]+",
        r"\btelegram\b",
        r"\bwhatsapp\b",
        r"\bsupabase\b",
    )
]
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
PHONE_RE = re.compile(r"\+1\d{10}\b")
DATE_RE = re.compile(r"\b(20\d{2})-\d{2}-\d{2}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(20\d{2})\b")
ID_VALUE_RE = re.compile(r'"(?:id|thread_id)"\s*:\s*"([^"]+)"')


def fixture_files() -> list[Path]:
    files: list[Path] = []
    for root in PUBLIC_FIXTURE_ROOTS:
        files.extend(path for path in root.rglob("*") if path.is_file())
    return sorted(files)


def test_public_fixtures_do_not_contain_hard_private_patterns() -> None:
    for path in fixture_files():
        text = path.read_text()
        for pattern in FORBIDDEN_PATTERNS:
            assert not pattern.search(text), f"{path} matched {pattern.pattern}"


def test_public_fixture_emails_are_example_or_intentional_bad_fixture() -> None:
    for path in fixture_files():
        text = path.read_text()
        for match in EMAIL_RE.finditer(text):
            email = match.group(0).lower()
            domain = match.group(1).lower()
            assert domain in ALLOWED_EMAIL_DOMAINS or email in ALLOWED_NON_EXAMPLE_EMAILS, (
                f"{path} contains non-synthetic email {email}"
            )


def test_public_fixture_phone_numbers_use_synthetic_range() -> None:
    for path in fixture_files():
        text = path.read_text()
        for phone in PHONE_RE.findall(text):
            assert phone.startswith("+1555010"), f"{path} contains non-synthetic phone {phone}"


def test_public_fixture_dates_are_fake_future_dates() -> None:
    for path in fixture_files():
        text = path.read_text()
        for match in DATE_RE.finditer(text):
            year = int(match.group(1) or match.group(2))
            assert year >= 2030, f"{path} contains pre-2030 fixture date {match.group(0)}"


def test_public_fixture_json_ids_are_obviously_synthetic() -> None:
    allowed_prefixes = ("demo_", "evt_demo_", "msg_demo_", "thr_demo_", "commit-demo-")
    for path in fixture_files():
        if path.suffix not in {".json", ".jsonl"}:
            continue
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            json.loads(line) if path.suffix == ".jsonl" else None
        for identifier in ID_VALUE_RE.findall(path.read_text()):
            assert identifier.startswith(allowed_prefixes), f"{path} has non-synthetic id {identifier}"


def test_public_fixture_names_stay_on_allowlist() -> None:
    title_case_phrases: set[str] = set()
    for path in fixture_files():
        for line in path.read_text().splitlines():
            title_case_phrases.update(
                re.findall(r"\b[A-Z][a-z]+(?:[ \t]+[A-Z][a-z]+){1,3}\b", line)
            )
    ignored = {
        "Demo Agent Identity",
        "Demo Agent Operating",
        "Demo Tool Contracts",
        "Working Context",
        "Current Synthetic Contacts",
        "Synthetic Contacts",
        "Synthetic Meeting Transcript",
        "Draft Update",
        "Gate Check",
        "Boot Payload",
        "Monday April",
        "Tuesday April",
        "Date Monday April",
        "Available Public",
        "Meeting Transcript",
        "Operating Rules",
        "Tool Contracts",
    }
    unexpected = {
        phrase
        for phrase in title_case_phrases
        if phrase not in ALLOWED_NAMES and phrase not in ignored and not phrase.startswith("Demo Agent")
    }
    assert not unexpected, f"unexpected title-case fixture names: {sorted(unexpected)}"
