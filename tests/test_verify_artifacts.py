import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = ROOT / "tools" / "verify_artifacts.py"
TITLE = "《OpenClaw 入门到精通》"


def load_verifier():
    if not VERIFIER_PATH.is_file():
        raise AssertionError("tools/verify_artifacts.py must exist")
    spec = importlib.util.spec_from_file_location("verify_artifacts", VERIFIER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("tools/verify_artifacts.py must be importable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ArtifactVerifierTests(unittest.TestCase):
    def test_html_requires_a_nonempty_file_with_the_exact_title(self):
        verifier = load_verifier()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            html = root / "book.html"
            html.write_text(
                f"<!doctype html><html><head><title>{TITLE}</title></head><body>book</body></html>",
                encoding="utf-8",
            )
            verifier.verify_html(html, TITLE)

            html.write_text("<title>Wrong book</title>", encoding="utf-8")
            with self.assertRaises(verifier.ArtifactVerificationError):
                verifier.verify_html(html, TITLE)

            html.write_text("", encoding="utf-8")
            with self.assertRaises(verifier.ArtifactVerificationError):
                verifier.verify_html(html, TITLE)

    def test_pdf_requires_signature_and_exact_metadata_or_visible_title(self):
        verifier = load_verifier()
        with tempfile.TemporaryDirectory() as directory:
            pdf = Path(directory) / "book.pdf"
            pdf.write_bytes(b"%PDF-1.4\nfixture")
            with patch.object(verifier.shutil, "which", return_value="/usr/bin/tool"), patch.object(
                verifier,
                "command_output",
                return_value=f"Title: {TITLE}\n",
            ):
                verifier.verify_pdf(pdf, TITLE)

            pdf.write_bytes(b"not a pdf")
            with self.assertRaises(verifier.ArtifactVerificationError):
                verifier.verify_pdf(pdf, TITLE)

    def test_checksum_manifest_is_sorted_portable_and_revalidated(self):
        verifier = load_verifier()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdf = root / "book.pdf"
            html = root / "book.html"
            manifest = root / "SHA256SUMS"
            pdf.write_bytes(b"pdf")
            html.write_bytes(b"html")

            verifier.write_checksums([pdf, html], manifest)
            lines = manifest.read_text(encoding="utf-8").splitlines()
            self.assertEqual([line.split("  ", 1)[1] for line in lines], ["book.html", "book.pdf"])
            verifier.verify_checksums(manifest)

            pdf.write_bytes(b"changed")
            with self.assertRaises(verifier.ArtifactVerificationError):
                verifier.verify_checksums(manifest)


if __name__ == "__main__":
    unittest.main()
