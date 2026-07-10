import os
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_PDF = ROOT / "tools" / "build_pdf.py"

FAKE_MDPRESS = r'''#!/usr/bin/env python3
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

args = sys.argv[1:]
output = Path(args[args.index("--output") + 1])
state = Path(os.environ["FAKE_MDPRESS_STATE"])
attempt = int(state.read_text(encoding="utf-8")) + 1 if state.exists() else 1
state.write_text(str(attempt), encoding="utf-8")
mode = os.environ["FAKE_MDPRESS_MODE"]

if mode == "retry-success":
    if attempt == 1:
        print("transient renderer failure", file=sys.stderr)
        raise SystemExit(7)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(b"%PDF-1.4\nretry success\n")
    print("second attempt succeeded")
    raise SystemExit(0)

if mode == "double-failure":
    print(f"permanent renderer failure {attempt}", file=sys.stderr)
    raise SystemExit(9)

if mode == "missing-output":
    print("reported success without an artifact")
    raise SystemExit(0)

if mode == "timeout":
    child_code = r''' + "'''" + r'''
import os
import signal
import time
from pathlib import Path

pid_path = Path(os.environ["FAKE_CHILD_PID"])
marker_path = Path(os.environ["FAKE_CHILD_TERMINATED"])
pid_path.write_text(str(os.getpid()), encoding="utf-8")

def terminate(_signum, _frame):
    marker_path.write_text("terminated", encoding="utf-8")
    raise SystemExit(0)

signal.signal(signal.SIGTERM, terminate)
while True:
    time.sleep(0.1)
''' + "'''" + r'''
    subprocess.Popen([sys.executable, "-c", child_code], env=os.environ.copy())
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    while True:
        time.sleep(0.1)

raise SystemExit(f"unknown mode: {mode}")
'''


class BuildPdfTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir()
        self.fake_mdpress = self.bin_dir / "mdpress"
        self.fake_mdpress.write_text(FAKE_MDPRESS, encoding="utf-8")
        self.fake_mdpress.chmod(0o755)
        self.state = self.root / "attempts.txt"
        self.output = self.root / "dist" / "book.pdf"
        self.logs = self.root / "logs"
        self.child_pid = self.root / "child.pid"
        self.child_terminated = self.root / "child-terminated.txt"

    def tearDown(self):
        if self.child_pid.exists():
            try:
                os.kill(int(self.child_pid.read_text(encoding="utf-8")), signal.SIGKILL)
            except (ProcessLookupError, ValueError):
                pass
        self.temp.cleanup()

    def run_builder(self, mode, *, attempts=2, timeout=2.0, terminate_grace=0.2):
        env = os.environ.copy()
        env.update(
            {
                "PATH": f"{self.bin_dir}:{env.get('PATH', '')}",
                "FAKE_MDPRESS_MODE": mode,
                "FAKE_MDPRESS_STATE": str(self.state),
                "FAKE_CHILD_PID": str(self.child_pid),
                "FAKE_CHILD_TERMINATED": str(self.child_terminated),
            }
        )
        return subprocess.run(
            [
                sys.executable,
                str(BUILD_PDF),
                "--output",
                str(self.output),
                "--log-dir",
                str(self.logs),
                "--attempts",
                str(attempts),
                "--timeout",
                str(timeout),
                "--retry-delay",
                "0",
                "--terminate-grace",
                str(terminate_grace),
            ],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_retries_once_then_succeeds(self):
        result = self.run_builder("retry-success")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(self.output.is_file())
        self.assertEqual(self.state.read_text(encoding="utf-8"), "2")
        self.assertIn("transient renderer failure", (self.logs / "attempt-1.log").read_text())
        self.assertIn("second attempt succeeded", (self.logs / "attempt-2.log").read_text())

    def test_double_failure_keeps_both_attempt_logs(self):
        result = self.run_builder("double-failure")

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        first_log = self.logs / "attempt-1.log"
        second_log = self.logs / "attempt-2.log"
        self.assertTrue(first_log.is_file(), result.stdout + result.stderr)
        self.assertTrue(second_log.is_file(), result.stdout + result.stderr)
        self.assertIn("permanent renderer failure 1", first_log.read_text())
        self.assertIn("permanent renderer failure 2", second_log.read_text())
        self.assertIn(str(first_log), result.stderr)
        self.assertIn(str(second_log), result.stderr)

    @unittest.skipIf(os.name == "nt", "POSIX process-group behavior")
    def test_timeout_terminates_the_whole_process_group(self):
        started = time.monotonic()
        result = self.run_builder("timeout", attempts=1, timeout=0.4, terminate_grace=0.4)

        self.assertNotEqual(result.returncode, 0)
        self.assertLess(time.monotonic() - started, 3)
        self.assertTrue(self.child_pid.is_file(), result.stdout + result.stderr)
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline and not self.child_terminated.exists():
            time.sleep(0.05)
        self.assertEqual(self.child_terminated.read_text(encoding="utf-8"), "terminated")
        self.assertIn("timed out", (self.logs / "attempt-1.log").read_text())

    def test_success_without_output_is_a_failure(self):
        result = self.run_builder("missing-output", attempts=1)

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        self.assertIn("did not create a non-empty PDF", result.stderr)
        self.assertIn(
            "did not create a non-empty PDF",
            (self.logs / "attempt-1.log").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
