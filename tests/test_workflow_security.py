import json
import os
import re
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
WORKFLOWS = tuple(sorted(WORKFLOW_DIR.glob("*.y*ml")))
BUILD_WORKFLOWS = tuple(
    WORKFLOW_DIR / name for name in ("auto-release.yml", "ci.yaml", "preview-pdf.yml")
)
ACTION_PINS = {
    "actions/attest-build-provenance": (
        "0f67c3f4856b2e3261c31976d6725780e5e4c373",
        "v4.1.1",
    ),
    "actions/checkout": ("9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0", "v7.0.0"),
    "actions/download-artifact": (
        "3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
        "v8.0.1",
    ),
    "actions/upload-artifact": (
        "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
        "v7.0.1",
    ),
    "browser-actions/setup-chrome": (
        "2e1d749697dd1612b833dba4a722266286fbefcd",
        "v2.1.2",
    ),
    "dependabot/fetch-metadata": (
        "25dd0e34f4fe68f24cc83900b1fe3fe149efef98",
        "v3.1.0",
    ),
    "softprops/action-gh-release": (
        "718ea10b132b3b2eba29c1007bb80653f286566b",
        "v3.0.1",
    ),
}

TEST_REPOSITORY = "owner/repo"
TEST_SHA = "a" * 40
GET_REF_COMMAND = [
    "api",
    "--include",
    "--method",
    "GET",
    f"repos/{TEST_REPOSITORY}/git/ref/tags/preview-pdf",
]
PATCH_REF_COMMAND = [
    "api",
    "--silent",
    "--method",
    "PATCH",
    f"repos/{TEST_REPOSITORY}/git/refs/tags/preview-pdf",
    "--raw-field",
    f"sha={TEST_SHA}",
    "--field",
    "force=true",
]
POST_REF_COMMAND = [
    "api",
    "--silent",
    "--method",
    "POST",
    f"repos/{TEST_REPOSITORY}/git/refs",
    "--raw-field",
    "ref=refs/tags/preview-pdf",
    "--raw-field",
    f"sha={TEST_SHA}",
]
VIEW_RELEASE_COMMAND = ["release", "view", "preview-pdf"]
EDIT_RELEASE_COMMAND = [
    "release",
    "edit",
    "preview-pdf",
    "--title",
    "Latest Preview PDF",
    "--notes-file",
    "dist/release-notes.md",
    "--prerelease",
]
CREATE_RELEASE_COMMAND = [
    "release",
    "create",
    "preview-pdf",
    "--title",
    "Latest Preview PDF",
    "--notes-file",
    "dist/release-notes.md",
    "--prerelease",
    "--latest=false",
    "--verify-tag",
]

FAKE_GH = r'''#!/usr/bin/env python3
import json
import os
import sys

args = sys.argv[1:]
with open(os.environ["GH_LOG"], "a", encoding="utf-8") as stream:
    stream.write(json.dumps(args) + "\n")

scenario = os.environ["GH_SCENARIO"]
repository = "owner/repo"
sha = "a" * 40
reasons = {
    "401": "Unauthorized",
    "403": "Forbidden",
    "404": "Not Found",
    "429": "Too Many Requests",
    "503": "Service Unavailable",
}

get_ref = ["api", "--include", "--method", "GET", f"repos/{repository}/git/ref/tags/preview-pdf"]
patch_ref = [
    "api", "--silent", "--method", "PATCH",
    f"repos/{repository}/git/refs/tags/preview-pdf",
    "--raw-field", f"sha={sha}", "--field", "force=true",
]
post_ref = [
    "api", "--silent", "--method", "POST", f"repos/{repository}/git/refs",
    "--raw-field", "ref=refs/tags/preview-pdf", "--raw-field", f"sha={sha}",
]
view_release = ["release", "view", "preview-pdf"]
edit_release = [
    "release", "edit", "preview-pdf", "--title", "Latest Preview PDF",
    "--notes-file", "dist/release-notes.md", "--prerelease",
]
create_release = [
    "release", "create", "preview-pdf", "--title", "Latest Preview PDF",
    "--notes-file", "dist/release-notes.md", "--prerelease",
    "--latest=false", "--verify-tag",
]

def fail_http(code):
    print(f"HTTP/2.0 {code} {reasons[code]}")
    print(f"fake gh HTTP {code}", file=sys.stderr)
    raise SystemExit(1)

if os.environ.get("GH_REPO") != repository:
    print("fake gh requires explicit GH_REPO", file=sys.stderr)
    raise SystemExit(2)

if args == get_ref:
    if scenario.startswith("ref_network"):
        print("fake gh network failure", file=sys.stderr)
        raise SystemExit(1)
    for code in reasons:
        if scenario.startswith(f"ref_{code}"):
            fail_http(code)
    print("HTTP/2.0 200 OK")
    print('Content-Type: application/json\n\n{"ref":"refs/tags/preview-pdf"}')
    raise SystemExit(0)

if args in (patch_ref, post_ref, edit_release, create_release):
    raise SystemExit(0)

if args == view_release:
    if "release_missing" in scenario:
        print("release not found", file=sys.stderr)
        raise SystemExit(1)
    if "release_network" in scenario:
        print("fake release network failure", file=sys.stderr)
        raise SystemExit(1)
    for code in reasons:
        if f"release_{code}" in scenario:
            print(f"fake release HTTP {code}", file=sys.stderr)
            raise SystemExit(1)
    raise SystemExit(0)

print(f"unexpected gh argv: {args!r}", file=sys.stderr)
raise SystemExit(2)
'''


def job_block(workflow_text, job_name):
    match = re.search(
        rf"(?ms)^  {re.escape(job_name)}:\n.*?(?=^  [A-Za-z0-9_-]+:\n|\Z)",
        workflow_text,
    )
    if match is None:
        raise AssertionError(f"workflow must define the {job_name!r} job")
    return match.group(0)


def workflow_step_script(workflow_text, step_name):
    marker = f"      - name: {step_name}\n"
    if marker not in workflow_text:
        raise AssertionError(f"workflow must define the {step_name!r} step")
    start = workflow_text.index(marker) + len(marker)
    run_marker = "        run: |\n"
    script_start = workflow_text.index(run_marker, start) + len(run_marker)
    script_end = workflow_text.find("\n      - name:", script_start)
    if script_end < 0:
        script_end = len(workflow_text)
    return textwrap.dedent(workflow_text[script_start:script_end])


def workflow_step_scripts_in_document_order(workflow_text, step_names):
    for name in step_names:
        marker = f"      - name: {name}\n"
        if marker not in workflow_text:
            raise AssertionError(f"workflow must define the {name!r} step")
    ordered_names = sorted(
        step_names,
        key=lambda name: workflow_text.index(f"      - name: {name}\n"),
    )
    return tuple(workflow_step_script(workflow_text, name) for name in ordered_names)


class WorkflowSecurityTests(unittest.TestCase):
    def test_inventory_actions_and_checkout_credentials_are_exact(self):
        self.assertEqual(
            {path.name for path in WORKFLOWS},
            {"auto-release.yml", "ci.yaml", "dependabot-automerge.yml", "preview-pdf.yml"},
        )
        for workflow in WORKFLOWS:
            with self.subTest(workflow=workflow.name):
                text = workflow.read_text(encoding="utf-8")
                self.assertRegex(text.split("\njobs:", 1)[0], r"(?m)^permissions: \{\}$")
                uses_lines = [line.strip() for line in text.splitlines() if "uses:" in line]
                self.assertGreater(len(uses_lines), 0)
                for line in uses_lines:
                    match = re.search(
                        r"uses:\s+(?P<action>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@"
                        r"(?P<sha>[0-9a-f]{40})\s+#\s+(?P<version>v\d+\.\d+\.\d+)\s*$",
                        line,
                    )
                    self.assertIsNotNone(match, line)
                    action = match.group("action")
                    self.assertIn(action, ACTION_PINS)
                    self.assertEqual(
                        (match.group("sha"), match.group("version")),
                        ACTION_PINS[action],
                    )
                if "actions/checkout@" in text:
                    index = text.index("actions/checkout@")
                    self.assertIn("persist-credentials: false", text[index : index + 240])

    def test_jobs_use_minimum_permissions_and_verified_artifact_handoffs(self):
        ci = (WORKFLOW_DIR / "ci.yaml").read_text(encoding="utf-8")
        release = (WORKFLOW_DIR / "auto-release.yml").read_text(encoding="utf-8")
        preview = (WORKFLOW_DIR / "preview-pdf.yml").read_text(encoding="utf-8")
        dependabot = (WORKFLOW_DIR / "dependabot-automerge.yml").read_text(encoding="utf-8")

        self.assertIn("permissions:\n      contents: read", job_block(ci, "build"))
        release_build = job_block(release, "build")
        release_publish = job_block(release, "release")
        preview_build = job_block(preview, "build")
        preview_publish = job_block(preview, "publish")

        for build in (release_build, preview_build):
            self.assertIn("permissions:\n      contents: read", build)
            self.assertNotIn("contents: write", build)
            self.assertIn("actions/upload-artifact@", build)

        self.assertIn("needs: build", release_publish)
        self.assertIn("contents: write", release_publish)
        self.assertIn("id-token: write", release_publish)
        self.assertIn("attestations: write", release_publish)
        self.assertIn("actions/download-artifact@", release_publish)

        self.assertIn("needs: build", preview_publish)
        self.assertIn("permissions:\n      contents: write", preview_publish)
        self.assertNotIn("id-token: write", preview_publish)
        self.assertNotIn("attestations: write", preview_publish)
        self.assertIn("actions/download-artifact@", preview_publish)
        self.assertNotIn("GH_TOKEN", preview_build)
        self.assertNotIn("github.token", preview_build)
        self.assertIn("GH_TOKEN: ${{ github.token }}", preview_publish)
        self.assertIn("GH_REPO: ${{ github.repository }}", preview_publish)
        for forbidden in ("actions/checkout@", "mdpress", "npm ", "curl ", "sudo ", "python3 ", "tools/"):
            self.assertNotIn(forbidden, preview_publish)

        dependabot_job = job_block(dependabot, "dependabot")
        self.assertIn("contents: write", dependabot_job)
        self.assertIn("pull-requests: write", dependabot_job)

    def test_dependencies_are_checksum_verified_and_mermaid_is_lockfile_backed(self):
        package_path = ROOT / "package.json"
        lock_path = ROOT / "package-lock.json"
        self.assertTrue(package_path.is_file(), "package.json must lock Mermaid")
        self.assertTrue(lock_path.is_file(), "package-lock.json must be committed")
        package = json.loads(package_path.read_text(encoding="utf-8"))
        self.assertEqual(package["devDependencies"]["@mermaid-js/mermaid-cli"], "11.16.0")
        self.assertEqual(package["devDependencies"]["puppeteer"], "24.43.1")
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(
            lock["packages"]["node_modules/@mermaid-js/mermaid-cli"]["version"],
            "11.16.0",
        )
        self.assertEqual(lock["packages"]["node_modules/puppeteer"]["version"], "24.43.1")
        self.assertNotIn("package-lock.json", (ROOT / ".gitignore").read_text(encoding="utf-8"))

        for workflow in BUILD_WORKFLOWS:
            with self.subTest(workflow=workflow.name):
                text = workflow.read_text(encoding="utf-8")
                self.assertIn("npm ci", text)
                self.assertNotRegex(text, r"npm install\s+--global\s+@mermaid-js/mermaid-cli")
                self.assertIn("MDPRESS_SHA256", text)
                self.assertIn("PANDOC_SHA256", text)
                self.assertIn("curl -fsSL --retry 3", text)
                self.assertIn("sha256sum -c -", text)
                self.assertIn('extract_dir="$(mktemp -d)"', text)
                self.assertIn("node_modules/.bin", text)

    def test_all_builds_reuse_bounded_pdf_builder_and_verify_pdf_html_sha(self):
        builder = (ROOT / "tools" / "build_pdf.py").read_text(encoding="utf-8")
        mermaid_renderer = (ROOT / "tools" / "render_mermaid.py").read_text(encoding="utf-8")
        self.assertNotIn("pkill", builder)
        self.assertNotIn("pkill", mermaid_renderer)
        for workflow in BUILD_WORKFLOWS:
            with self.subTest(workflow=workflow.name):
                text = workflow.read_text(encoding="utf-8")
                self.assertIn("python3 tools/build_pdf.py", text)
                self.assertNotRegex(text, r"(?m)^\s*mdpress build\b")
                self.assertIn("--log-dir dist/build-logs", text)
                self.assertNotIn("pkill", text)
                self.assertIn("python3 -m unittest discover -s tests -v", text)
                self.assertIn("tools/render_mermaid.py", text)
                self.assertIn("tools/build_html_reader.py", text)
                self.assertIn("tools/verify_artifacts.py", text)
                self.assertIn("--pdf", text)
                self.assertIn("--html", text)
                self.assertIn("SHA256SUMS", text)
                self.assertIn("if-no-files-found: error", text)
                self.assertNotIn("continue-on-error: true", text)

    def test_release_has_formal_provenance_for_every_verified_artifact(self):
        release = (WORKFLOW_DIR / "auto-release.yml").read_text(encoding="utf-8")
        build = job_block(release, "build")
        publish = job_block(release, "release")

        self.assertNotIn("attest-build-provenance", build)
        self.assertIn(
            "actions/attest-build-provenance@0f67c3f4856b2e3261c31976d6725780e5e4c373 # v4.1.1",
            publish,
        )
        self.assertIn("subject-path: |", publish)
        self.assertIn("dist/oc_guide-*.pdf", publish)
        self.assertIn("dist/oc_guide-*.html", publish)
        self.assertIn("dist/SHA256SUMS", publish)
        self.assertLess(publish.index("sha256sum -c SHA256SUMS"), publish.index("attest-build-provenance"))

    def test_preview_publish_steps_follow_tag_release_asset_order(self):
        preview = (WORKFLOW_DIR / "preview-pdf.yml").read_text(encoding="utf-8")
        for name in (
            "Synchronize mutable preview tag",
            "Create or update preview release",
            "Upload verified preview artifacts",
        ):
            self.assertIn(f"      - name: {name}\n", preview)
        synchronize = preview.index("      - name: Synchronize mutable preview tag\n")
        release = preview.index("      - name: Create or update preview release\n")
        upload = preview.index("      - name: Upload verified preview artifacts\n")
        self.assertLess(synchronize, release)
        self.assertLess(release, upload)

    def run_preview_scripts(self, scenario, *, repository=TEST_REPOSITORY, sha=TEST_SHA):
        preview = (WORKFLOW_DIR / "preview-pdf.yml").read_text(encoding="utf-8")
        scripts = workflow_step_scripts_in_document_order(
            preview,
            ("Synchronize mutable preview tag", "Create or update preview release"),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_gh = root / "gh"
            fake_gh.write_text(FAKE_GH, encoding="utf-8")
            fake_gh.chmod(0o755)
            log = root / "commands.jsonl"
            env = os.environ.copy()
            env.update(
                {
                    "PATH": f"{root}:{env.get('PATH', '')}",
                    "GH_LOG": str(log),
                    "GH_SCENARIO": scenario,
                    "GH_TOKEN": "test-token",
                    "GH_REPO": repository,
                    "GITHUB_REPOSITORY": repository,
                    "GITHUB_SHA": sha,
                }
            )
            result = None
            for script in scripts:
                result = subprocess.run(
                    ["/bin/bash", "-c", script],
                    cwd=ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    break
            commands = []
            if log.exists():
                commands = [json.loads(line) for line in log.read_text().splitlines()]
            return result, commands

    def test_mutable_preview_updates_existing_tag_and_release(self):
        result, commands = self.run_preview_scripts("ref_200_release_exists")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            commands,
            [GET_REF_COMMAND, PATCH_REF_COMMAND, VIEW_RELEASE_COMMAND, EDIT_RELEASE_COMMAND],
        )

    def test_mutable_preview_creates_only_on_explicit_not_found(self):
        result, commands = self.run_preview_scripts("ref_404_release_missing")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            commands,
            [GET_REF_COMMAND, POST_REF_COMMAND, VIEW_RELEASE_COMMAND, CREATE_RELEASE_COMMAND],
        )
        self.assertNotIn("--target", [arg for command in commands for arg in command])

    def test_preview_rejects_invalid_repository_and_sha_before_calling_gh(self):
        cases = (
            ("owner/repo/extra", TEST_SHA, "Invalid GITHUB_REPOSITORY"),
            (TEST_REPOSITORY, "a" * 39, "Invalid GITHUB_SHA"),
        )
        for repository, sha, message in cases:
            with self.subTest(repository=repository, sha=sha):
                result, commands = self.run_preview_scripts(
                    "ref_200_release_exists", repository=repository, sha=sha
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(commands, [])
                self.assertIn(message, result.stderr)

    def test_preview_tag_lookup_fails_closed_on_non_404_errors(self):
        for scenario in ("ref_401", "ref_403", "ref_429", "ref_503", "ref_network"):
            with self.subTest(scenario=scenario):
                result, commands = self.run_preview_scripts(scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(commands, [GET_REF_COMMAND])
                expected = "network failure" if scenario.endswith("network") else scenario.removeprefix("ref_")
                self.assertIn(expected, result.stderr)

    def test_preview_release_lookup_fails_closed_except_exact_not_found(self):
        scenarios = (
            "ref_200_release_401",
            "ref_200_release_403",
            "ref_200_release_404",
            "ref_200_release_429",
            "ref_200_release_503",
            "ref_200_release_network",
        )
        for scenario in scenarios:
            with self.subTest(scenario=scenario):
                result, commands = self.run_preview_scripts(scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(
                    commands,
                    [GET_REF_COMMAND, PATCH_REF_COMMAND, VIEW_RELEASE_COMMAND],
                )
                expected = "network failure" if scenario.endswith("network") else scenario.rsplit("release_", 1)[1]
                self.assertIn(expected, result.stderr)


if __name__ == "__main__":
    unittest.main()
