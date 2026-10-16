"""Smoke tests for local third-party archive intake. No network or downloads."""
from __future__ import annotations
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "import_cc0_pack.py"

class PackImporterTests(unittest.TestCase):
    def invoke(self, archive: Path, output: Path, source: str = "kenney-ui"):
        return subprocess.run(
            ["python3", str(SCRIPT), source, str(archive), "--confirm-license", "--output", str(output)],
            text=True, capture_output=True, check=False,
        )

    def test_valid_archive_has_provenance_and_only_safe_files(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            archive = root / "valid.zip"
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("images/button.png", b"\x89PNG\r\n\x1a\nprototype")
                z.writestr("scripts/unsafe.js", b"alert('danger')")
                z.writestr("license.txt", "CC0 from original source")
            result = self.invoke(archive, root / "output")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "output" / "kenney-ui" / "images" / "button.png").exists())
            self.assertTrue((root / "output" / "kenney-ui" / "manifest.json").exists())
            self.assertFalse((root / "output" / "kenney-ui" / "scripts" / "unsafe.js").exists())

    def test_path_traversal_is_rejected_without_writing_outside_target(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            archive = root / "bad.zip"
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("../escaped.png", b"untrusted")
            result = self.invoke(archive, root / "output")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / "escaped.png").exists())

    def test_requires_rights_confirmation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            archive = root / "valid.zip"
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("license.txt", "test")
            result = subprocess.run(
                ["python3", str(SCRIPT), "kenney-ui", str(archive)],
                text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("confirm-license", result.stderr)

if __name__ == "__main__":
    unittest.main()
