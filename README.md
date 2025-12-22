# HealthArchive datasets (metadata-only)

This repository publishes **versioned, citable dataset releases** for
HealthArchive.ca as **metadata-only** exports.

- Source project: https://healtharchive.ca
- Public API: https://api.healtharchive.ca/api
- Data dictionary: https://www.healtharchive.ca/exports

## What this is / isn’t

- This is an archival metadata dataset intended for reproducibility and auditability.
- It is **not medical advice** and **not current guidance**.
- It is **not** an official government resource and is not affiliated with any public health agency.
- Releases do **not** include raw HTML bodies or full diff bodies.

## Release contents (current)

Each GitHub Release contains:

- `healtharchive-snapshots.jsonl.gz` — snapshot metadata export
- `healtharchive-changes.jsonl.gz` — change-event metadata export
- `manifest.json` — release metadata (API base, counts, ranges, checksums)
- `SHA256SUMS` — SHA-256 checksums for the files above

## Tag naming

Tags are date-based for future flexibility:

- `healtharchive-dataset-YYYY-MM-DD`

## How releases are produced

Releases are generated automatically by GitHub Actions by calling the public export endpoints:

- `GET https://api.healtharchive.ca/api/exports/snapshots`
- `GET https://api.healtharchive.ca/api/exports/changes`

The workflow paginates using `afterId` and writes a single gzipped JSONL for each export.

## Release schedule

- Quarterly (Jan/Apr/Jul/Oct) via GitHub Actions.
- Note: GitHub may disable scheduled workflows after 60 days of repo inactivity. This repo includes a weekly keepalive workflow to prevent that.
