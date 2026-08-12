from __future__ import annotations

import gzip
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build_release
from scripts.export_schema import CHANGE_EXPORT_FIELDS, SNAPSHOT_EXPORT_FIELDS

REPO_ROOT = Path(__file__).resolve().parents[1]


class ExportSchemaTests(unittest.TestCase):
    def _build_snapshot_row(self, row: dict[str, object]) -> None:
        payload = io.BytesIO((json.dumps(row) + "\n").encode("utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "snapshots.jsonl.gz"
            with patch.object(build_release, "_http_ndjson_stream", return_value=payload):
                build_release._download_export_to_gzip_jsonl(
                    api_base="https://api.healtharchive.ca",
                    path="/api/exports/snapshots",
                    export_name="snapshots",
                    id_field="snapshot_id",
                    out_path=out_path,
                    limit=1,
                    timeout=1,
                    user_agent="schema-test",
                    max_requests=1,
                )

            with gzip.open(out_path, "rt", encoding="utf-8") as artifact:
                self.assertEqual(json.loads(artifact.readline()), row)

    def test_expected_field_sets_match_rights_inventory(self) -> None:
        rights = (REPO_ROOT / "RIGHTS.md").read_text(encoding="utf-8")
        sections = {
            "Snapshot export": ("Change export", SNAPSHOT_EXPORT_FIELDS),
            "Change export": ("Release-wrapper fields", CHANGE_EXPORT_FIELDS),
        }

        self.assertEqual(len(SNAPSHOT_EXPORT_FIELDS), 15)
        self.assertEqual(len(CHANGE_EXPORT_FIELDS), 24)
        for heading, (next_heading, expected) in sections.items():
            section = rights.split(f"## {heading}", maxsplit=1)[1].split(
                f"## {next_heading}", maxsplit=1
            )[0]
            documented = set(re.findall(r"^\| `([^`]+)` \|", section, flags=re.MULTILINE))
            self.assertEqual(documented, expected)

    def test_builder_rejects_unexpected_field(self) -> None:
        row = dict.fromkeys(SNAPSHOT_EXPORT_FIELDS)
        row["snapshot_id"] = 1
        row["unreviewed_field"] = "unexpected"

        with self.assertRaisesRegex(ValueError, "unexpected fields: unreviewed_field"):
            self._build_snapshot_row(row)

    def test_builder_rejects_missing_field(self) -> None:
        row = dict.fromkeys(SNAPSHOT_EXPORT_FIELDS)
        row["snapshot_id"] = 1
        del row["title"]

        with self.assertRaisesRegex(ValueError, "missing fields: title"):
            self._build_snapshot_row(row)
