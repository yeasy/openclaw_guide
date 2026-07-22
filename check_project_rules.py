#!/usr/bin/env python3
"""Lightweight Markdown project checks for book repositories."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse
from datetime import date, datetime, timedelta


ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {
    ".agent",
    ".git",
    ".mdpress",
    "_book",
    "_site",
    "dist",
    "node_modules",
}
LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(([^)\s]+(?:\s+\"[^\"]*\")?)\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


VOLATILE_FACTS = Path("appendix/volatile_facts.md")


def check_volatile_facts(filepath=VOLATILE_FACTS, today=None):
    """Validate the dated snapshot that contains deliberately volatile claims."""
    path = Path(filepath)
    current_date = today or date.today()
    issues = []

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{path} [Volatile facts] Cannot read ledger: {exc}"]

    metadata = re.search(
        r"`verified_at`:\s*(\d{4}-\d{2}-\d{2})\s*·\s*"
        r"`expires_at`:\s*(\d{4}-\d{2}-\d{2})\s*·\s*"
        r"`ttl_days`:\s*(\d+)",
        content,
    )
    if metadata is None:
        return [
            f"{path} [Volatile facts] Missing verified_at, expires_at, or ttl_days metadata."
        ]

    try:
        verified_at = datetime.strptime(metadata.group(1), "%Y-%m-%d").date()
        expires_at = datetime.strptime(metadata.group(2), "%Y-%m-%d").date()
        ttl_days = int(metadata.group(3))
    except ValueError as exc:
        return [f"{path} [Volatile facts] Invalid metadata: {exc}"]

    if ttl_days != 30 or expires_at - verified_at != timedelta(days=30):
        issues.append(
            f"{path} [Volatile facts] Snapshot TTL must be exactly 30 days."
        )
    if verified_at > current_date:
        issues.append(
            f"{path} [Volatile facts] verified_at is in the future: {verified_at}."
        )
    if current_date > expires_at:
        issues.append(
            f"{path} [Volatile facts] Snapshot expired on {expires_at}."
        )

    statuses = re.findall(
        r"<!--\s*volatile-status:\s+id=[^\s]+\s+status=([^\s]+)\s*-->",
        content,
    )
    if not statuses:
        issues.append(f"{path} [Volatile facts] Missing volatile-status marker.")
    for status in statuses:
        if status == "open-conflict":
            issues.append(f"{path} [Volatile facts] Ledger has an unresolved conflict.")
        elif status not in {"current", "resolved-conflict"}:
            issues.append(
                f"{path} [Volatile facts] Unsupported volatile-status: {status}."
            )

    return issues


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def strip_fenced_blocks(text: str) -> str:
    output: list[str] = []
    in_fence = False
    fence_marker = ""
    fence_len = 0
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            char = marker[0]
            length = len(marker)
            if not in_fence:
                in_fence = True
                fence_marker = char
                fence_len = length
            elif char == fence_marker and length >= fence_len:
                in_fence = False
            output.append("")
            continue
        output.append("" if in_fence else line)
    return "\n".join(output)


def check_fences(path: Path, text: str) -> list[str]:
    issues: list[str] = []
    stack: list[tuple[str, int, int]] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        marker = match.group(1)
        char = marker[0]
        length = len(marker)
        if not stack:
            stack.append((char, length, line_no))
            continue
        open_char, open_len, _ = stack[-1]
        if char == open_char and length >= open_len:
            stack.pop()
        else:
            stack.append((char, length, line_no))
    for _, _, line_no in stack:
        issues.append(f"{path.relative_to(ROOT)}:{line_no}: unclosed fenced code block")
    return issues


def is_local_target(target: str) -> bool:
    parsed = urlparse(target)
    return not parsed.scheme and not parsed.netloc and not target.startswith("#")


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if " " in target and target.count('"') >= 2:
        target = target.split(" ", 1)[0]
    return unquote(target.split("#", 1)[0])


def check_links(path: Path, text: str) -> list[str]:
    issues: list[str] = []
    body = strip_fenced_blocks(text)
    for match in LINK_RE.finditer(body):
        raw_target = match.group(2).strip()
        target = normalize_target(raw_target)
        if not target or not is_local_target(raw_target):
            continue
        target_path = (path.parent / target).resolve()
        try:
            target_path.relative_to(ROOT)
        except ValueError:
            continue
        if not target_path.exists():
            line_no = body[: match.start()].count("\n") + 1
            issues.append(
                f"{path.relative_to(ROOT)}:{line_no}: missing local link target: {raw_target}"
            )
    return issues


def check_summary_links() -> list[str]:
    summary = ROOT / "SUMMARY.md"
    if not summary.exists():
        return []
    return check_links(summary, summary.read_text(encoding="utf-8", errors="ignore"))


def main() -> int:
    issues: list[str] = []
    files = iter_markdown_files()
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        issues.extend(check_fences(path, text))
        issues.extend(check_links(path, text))
    issues.extend(check_summary_links())
    issues.extend(check_volatile_facts())

    if issues:
        print("\n".join(sorted(set(issues))))
        print(f"\n{len(set(issues))} issue(s) found across {len(files)} Markdown files.")
        return 1
    print(f"All {len(files)} Markdown files passed project checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
