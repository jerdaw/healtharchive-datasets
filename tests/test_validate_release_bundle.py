from __future__ import annotations

import gzip
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import validate_release_bundle


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class ValidateReleaseBundleTests(unittest.TestCase):
    def _write_bundle(self, bundle_dir: Path, *, notes: dict[str, bool] | None = None) -> None:
        snapshots_path = bundle_dir / "healtharchive-snapshots.jsonl.gz"
        changes_path = bundle_dir / "healtharchive-changes.jsonl.gz"

        with gzip.open(snapshots_path, "wt", encoding="utf-8") as f:
            f.write(json.dumps({"snapshot_id": 1}) + "\n")
        with gzip.open(changes_path, "wt", encoding="utf-8") as f:
            f.write(json.dumps({"change_id": 1}) + "\n")

        default_notes = {
            "metadataOnly": True,
            "noRawHtml": True,
            "noDiffBodies": True,
            "notMedicalAdvice": True,
            "notCurrentGuidance": True,
        }
        if notes is not None:
            default_notes.update(notes)

        manifest = {
            "version": 1,
            "tag": "healtharchive-dataset-2026-01-01",
            "releasedAtUtc": "2026-01-01T00:00:00+00:00",
            "apiBase": "https://api.healtharchive.ca",
            "exportsManifest": {"enabled": True},
            "artifacts": {
                "snapshots": {
                    "path": "/api/exports/snapshots",
                    "idField": "snapshot_id",
                    "rows": 1,
                    "minId": 1,
                    "maxId": 1,
                    "limitPerRequest": 10000,
                    "requestsMade": 1,
                    "truncated": False,
                    "filename": snapshots_path.name,
                    "sha256": _sha256(snapshots_path),
                },
                "changes": {
                    "path": "/api/exports/changes",
                    "idField": "change_id",
                    "rows": 1,
                    "minId": 1,
                    "maxId": 1,
                    "limitPerRequest": 10000,
                    "requestsMade": 1,
                    "truncated": False,
                    "filename": changes_path.name,
                    "sha256": _sha256(changes_path),
                },
            },
            "notes": default_notes,
        }

        manifest_path = bundle_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8")

        sums_path = bundle_dir / "SHA256SUMS"
        sums_path.write_text(
            "\n".join(
                [
                    f"{_sha256(snapshots_path)}  {snapshots_path.name}",
                    f"{_sha256(changes_path)}  {changes_path.name}",
                    f"{_sha256(manifest_path)}  {manifest_path.name}",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def _run_validator(self, bundle_dir: Path) -> int:
        argv = ["validate_release_bundle.py", "--bundle-dir", str(bundle_dir)]
        with patch("sys.argv", argv):
            return validate_release_bundle.main()

    def test_valid_bundle_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle_dir = Path(tmp)
            self._write_bundle(bundle_dir)

            self.assertEqual(self._run_validator(bundle_dir), 0)

    def test_metadata_contract_notes_must_be_true(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle_dir = Path(tmp)
            self._write_bundle(bundle_dir, notes={"noRawHtml": False})

            with self.assertRaisesRegex(ValueError, "manifest.notes.noRawHtml must be true"):
                self._run_validator(bundle_dir)


if __name__ == "__main__":
    unittest.main()
