"""Smoke tests for the user-download pixel/audio intake (standard library only)."""
from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
import wave
import zipfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


def load_script(name):
    script = Path(__file__).resolve().parent / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PixelIntakeTest(unittest.TestCase):
    def test_reject_zip_slip_and_symlink(self):
        intake = load_script("intake_pixel_assets.py")
        self.assertIsNone(intake.safe_path("../private.png"))
        self.assertIsNone(intake.safe_path("/private.png"))
        self.assertIsNone(intake.safe_path("C:/private.png"))
        self.assertIsNotNone(intake.safe_path("map/house.png"))

    def test_zip_scan_review_and_import_only_safe_2d_data(self):
        intake = load_script("intake_pixel_assets.py")
        validator = load_script("validate_pixel_assets.py")
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            downloads = sandbox / "Downloads"
            downloads.mkdir()
            archive = downloads / "legal-city.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("sprites/cafe.png", b"\x89PNG\r\n\x1a\n" + b"stub art bytes")
                zf.writestr("meshes/nope.glb", b"3D not accepted")
                zf.writestr("malicious.sh", b"never extract")
                zf.writestr("LICENSE.txt", "CC0-1.0 test")
            bad = downloads / "unsafe.zip"
            with zipfile.ZipFile(bad, "w") as zf:
                zf.writestr("../escape.png", b"bad")
            private = sandbox / "assets" / "local-intake"
            public = sandbox / "assets" / "imported"
            with patch.object(intake, "PRIVATE", private), patch.object(intake, "REVIEWS", private / "reviews.json"), patch.object(intake, "PUBLIC", public), patch.object(intake, "ROOT", sandbox):
                with redirect_stdout(io.StringIO()):
                    intake.scan(downloads)
                report = intake.load()
                self.assertEqual(len(report["files"]), 2)
                good = next(x for x in report["files"] if x["name"] == "legal-city.zip")
                evil = next(x for x in report["files"] if x["name"] == "unsafe.zip")
                self.assertTrue(evil["issues"])
                good.update({
                    "approved": True,
                    "redistribute_public": True,
                    "license_id": "CC0-1.0",
                    "creator": "Example",
                    "source_url": "https://example.org/assets",
                    "license_evidence_url": "https://example.org/license",
                })
                intake.save(report)
                with redirect_stdout(io.StringIO()):
                    intake.import_approved()
                dirs = list(public.iterdir())
                self.assertEqual(len(dirs), 1)
                output = dirs[0]
                self.assertTrue((output / "pixel" / "sprites" / "cafe.png").is_file())
                self.assertFalse((output / "meshes" / "nope.glb").exists())
                self.assertFalse((output / "malicious.sh").exists())
                self.assertFalse((sandbox / "escape.png").exists())
                self.assertFalse((output / "legal-city.zip").exists())
                self.assertTrue((output / "SOURCE.json").is_file())
                with patch.object(validator, "IMPORTED", public), redirect_stdout(io.StringIO()):
                    self.assertEqual(validator.main(), 0)

    def test_loose_sound_is_accepted_but_restricted_license_is_not(self):
        intake = load_script("intake_pixel_assets.py")
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            downloads = sandbox / "Downloads"
            downloads.mkdir()
            sound = downloads / "cafe.wav"
            with wave.open(str(sound), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(22050)
                wav.writeframes(b"\x00\x00" * 220)
            private = sandbox / "assets" / "local-intake"
            public = sandbox / "assets" / "imported"
            with patch.object(intake, "PRIVATE", private), patch.object(intake, "REVIEWS", private / "reviews.json"), patch.object(intake, "PUBLIC", public), patch.object(intake, "ROOT", sandbox):
                with redirect_stdout(io.StringIO()):
                    intake.scan(downloads)
                report = intake.load()
                self.assertEqual(len(report["files"]), 1)
                report["files"][0].update({
                    "approved": True, "redistribute_public": True,
                    "license_id": "UNKNOWN-CUSTOM",
                    "source_url": "https://example.org/sound",
                    "license_evidence_url": "https://example.org/license",
                    "creator": "Test",
                })
                intake.save(report)
                with redirect_stdout(io.StringIO()):
                    intake.import_approved()
                self.assertFalse(public.exists() and list(public.iterdir()))


if __name__ == "__main__":
    unittest.main()
