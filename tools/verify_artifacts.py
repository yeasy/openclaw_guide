#!/usr/bin/env python3
"""Verify book artifact identity and maintain a portable SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path


class ArtifactVerificationError(ValueError):
    """Raised when a built artifact fails an identity or integrity check."""


def normalized_title(value: str) -> str:
    return " ".join(html.unescape(value).split())


def require_file(path: Path) -> None:
    if not path.is_file():
        raise ArtifactVerificationError(f"artifact is missing or not a file: {path}")
    if path.stat().st_size == 0:
        raise ArtifactVerificationError(f"artifact is empty: {path}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_html(path: Path, expected_title: str) -> None:
    require_file(path)
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<title(?:\s[^>]*)?>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    actual = normalized_title(match.group(1)) if match else ""
    expected = normalized_title(expected_title)
    if actual != expected:
        raise ArtifactVerificationError(
            f"HTML title mismatch for {path}: expected {expected!r}, got {actual!r}"
        )


def command_output(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise ArtifactVerificationError(f"command failed ({' '.join(command)}): {detail}")
    return result.stdout


def verify_pdf(path: Path, expected_title: str) -> None:
    require_file(path)
    if not path.read_bytes().startswith(b"%PDF-"):
        raise ArtifactVerificationError(f"artifact does not have a PDF signature: {path}")
    if shutil.which("pdfinfo") is None or shutil.which("pdftotext") is None:
        raise ArtifactVerificationError("pdfinfo and pdftotext are required for PDF verification")

    expected = normalized_title(expected_title)
    metadata = command_output(["pdfinfo", str(path)])
    match = re.search(r"(?m)^Title:\s*(.*)$", metadata)
    metadata_title = normalized_title(match.group(1)) if match else ""
    if metadata_title == expected:
        return

    visible_text = normalized_title(
        command_output(["pdftotext", "-f", "1", "-l", "2", str(path), "-"])
    )
    if expected not in visible_text:
        raise ArtifactVerificationError(
            f"PDF title mismatch for {path}: expected {expected!r}, "
            f"metadata title was {metadata_title!r}"
        )


def write_checksums(paths: list[Path], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for path in sorted(paths, key=lambda item: item.name):
        require_file(path)
        if path.parent.resolve() != destination.parent.resolve():
            raise ArtifactVerificationError(
                f"artifact {path} must be beside checksum manifest {destination}"
            )
        lines.append(f"{sha256_file(path)}  {path.name}\n")
    destination.write_text("".join(lines), encoding="utf-8")


def verify_checksums(manifest: Path) -> None:
    require_file(manifest)
    seen = set()
    for number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\]+)", line)
        if match is None:
            raise ArtifactVerificationError(f"invalid checksum line {number} in {manifest}")
        expected, filename = match.groups()
        if filename in seen:
            raise ArtifactVerificationError(f"duplicate checksum entry: {filename}")
        seen.add(filename)
        path = manifest.parent / filename
        require_file(path)
        actual = sha256_file(path)
        if actual != expected:
            raise ArtifactVerificationError(
                f"checksum mismatch for {path}: expected {expected}, got {actual}"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--html", type=Path)
    parser.add_argument("--checksums", type=Path)
    args = parser.parse_args()
    if args.pdf is None and args.html is None:
        parser.error("at least one of --pdf or --html is required")
    return args


def main() -> int:
    args = parse_args()
    artifacts = []
    try:
        if args.pdf is not None:
            verify_pdf(args.pdf, args.title)
            artifacts.append(args.pdf)
        if args.html is not None:
            verify_html(args.html, args.title)
            artifacts.append(args.html)
        if args.checksums is not None:
            write_checksums(artifacts, args.checksums)
            verify_checksums(args.checksums)
    except ArtifactVerificationError as error:
        print(f"artifact verification failed: {error}", file=sys.stderr)
        return 1

    for artifact in artifacts:
        print(f"verified artifact: {artifact}")
    if args.checksums is not None:
        print(f"verified checksums: {args.checksums}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
