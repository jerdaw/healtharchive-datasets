from __future__ import annotations

from typing import Any

SNAPSHOT_EXPORT_FIELDS = frozenset(
    {
        "snapshot_id",
        "source_code",
        "source_name",
        "captured_url",
        "normalized_url_group",
        "capture_timestamp_utc",
        "language",
        "status_code",
        "mime_type",
        "title",
        "capture_backend",
        "capture_fidelity",
        "job_id",
        "job_name",
        "snapshot_url",
    }
)

CHANGE_EXPORT_FIELDS = frozenset(
    {
        "change_id",
        "source_code",
        "source_name",
        "normalized_url_group",
        "from_snapshot_id",
        "to_snapshot_id",
        "from_capture_timestamp_utc",
        "to_capture_timestamp_utc",
        "from_job_id",
        "to_job_id",
        "change_type",
        "summary",
        "added_sections",
        "removed_sections",
        "changed_sections",
        "added_lines",
        "removed_lines",
        "change_ratio",
        "high_noise",
        "diff_truncated",
        "diff_version",
        "normalization_version",
        "computed_at_utc",
        "compare_url",
    }
)

EXPECTED_EXPORT_FIELDS = {
    "snapshots": SNAPSHOT_EXPORT_FIELDS,
    "changes": CHANGE_EXPORT_FIELDS,
}


def require_expected_export_fields(
    row: Any,
    *,
    export_name: str,
    context: str,
) -> dict[str, Any]:
    expected = EXPECTED_EXPORT_FIELDS.get(export_name)
    if expected is None:
        raise ValueError(f"Unknown export schema: {export_name}")
    if not isinstance(row, dict):
        raise ValueError(f"{export_name} export row at {context} must be a JSON object")

    actual = frozenset(row)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected:
        details: list[str] = []
        if missing:
            details.append(f"missing fields: {', '.join(missing)}")
        if unexpected:
            details.append(f"unexpected fields: {', '.join(unexpected)}")
        raise ValueError(
            f"{export_name} export schema mismatch at {context}: {'; '.join(details)}. "
            "Review the API change and update the expected schema and RIGHTS.md together."
        )

    return row
