#!/usr/bin/env python3
"""Build a PDF with bounded retries and process-scoped timeout cleanup."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


MAX_ATTEMPTS = 3


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def nonnegative_float(value: str) -> float:
    parsed = float(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must not be negative")
    return parsed


def append_log(stream, message: str) -> None:
    stream.write(f"\n[build_pdf] {message}\n")
    stream.flush()


def terminate_process_tree(process: subprocess.Popen, grace: float) -> None:
    """Terminate only the timed-out build's process group."""

    if os.name != "posix":
        process.terminate()
        try:
            process.wait(timeout=grace)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        return

    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        process.wait()
        return

    try:
        process.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def build_once(
    command: list[str],
    output: Path,
    log_path: Path,
    timeout: float,
    terminate_grace: float,
) -> tuple[bool, str]:
    output.unlink(missing_ok=True)
    with log_path.open("w", encoding="utf-8") as log:
        try:
            process = subprocess.Popen(
                command,
                stdout=log,
                stderr=subprocess.STDOUT,
                text=True,
                start_new_session=os.name == "posix",
            )
        except OSError as error:
            message = f"could not start mdpress: {error}"
            append_log(log, message)
            return False, message

        try:
            returncode = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            message = f"build timed out after {timeout:g} seconds"
            append_log(log, message)
            terminate_process_tree(process, terminate_grace)
            return False, message

        if returncode != 0:
            message = f"mdpress exited with status {returncode}"
            append_log(log, message)
            return False, message

        if not output.is_file() or output.stat().st_size == 0:
            message = f"mdpress did not create a non-empty PDF at {output}"
            append_log(log, message)
            return False, message

    return True, ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--log-dir", type=Path)
    parser.add_argument("--mdpress", default="mdpress")
    parser.add_argument("--attempts", type=int, choices=range(1, MAX_ATTEMPTS + 1), default=2)
    parser.add_argument("--timeout", type=positive_float, default=600.0)
    parser.add_argument("--retry-delay", type=nonnegative_float, default=5.0)
    parser.add_argument("--terminate-grace", type=positive_float, default=3.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    log_dir = (args.log_dir or output.parent / "build-logs").resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    command = [args.mdpress, "build", "--format", "pdf", "--output", str(output)]

    failures = []
    for attempt in range(1, args.attempts + 1):
        log_path = log_dir / f"attempt-{attempt}.log"
        succeeded, reason = build_once(
            command,
            output,
            log_path,
            args.timeout,
            args.terminate_grace,
        )
        if succeeded:
            print(f"PDF build succeeded on attempt {attempt}: {output}")
            return 0

        failures.append((log_path, reason))
        print(
            f"PDF build attempt {attempt} failed: {reason}; log retained at {log_path}",
            file=sys.stderr,
        )
        if attempt < args.attempts:
            time.sleep(args.retry_delay)

    output.unlink(missing_ok=True)
    print("PDF build failed after bounded retries.", file=sys.stderr)
    for log_path, _ in failures:
        print(f"- {log_path}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
