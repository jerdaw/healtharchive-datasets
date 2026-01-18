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

## Release integrity (required)

Each release build enforces:

- Bundle validation (`manifest.json` required fields + invariants, `truncated=false`)
- Artifact integrity (SHA-256 checksums match both `manifest.json` and `SHA256SUMS`)

If validation fails, the workflow aborts and does not publish/update a release.

## Release schedule

- Quarterly (Jan/Apr/Jul/Oct) via GitHub Actions.
- Note: GitHub may disable scheduled workflows after 60 days of repo inactivity. This repo includes a weekly keepalive workflow to prevent that.

## Verify a release (checksums)

Download the release assets into the same directory as `SHA256SUMS`, then verify:

```bash
sha256sum -c SHA256SUMS
```

If you only downloaded `SHA256SUMS`, the verification will fail because the referenced files are missing.

## Immutability / reruns

Dataset releases are treated as immutable research objects.

- Scheduled runs do not update an existing tag.
- If a publish run fails mid-flight, re-run via workflow dispatch and only enable “allow update existing” if you are intentionally recovering a partial/invalid release.

## Documentation hygiene

- Backend docs site (MkDocs): https://docs.healtharchive.ca (built from the backend repo)
- Canonical documentation guidelines: https://docs.healtharchive.ca/documentation-guidelines/
- Dataset docs guidelines (this repo): `DOCUMENTATION.md`

## Local dev (optional)

- Create venv: `make venv`
- Run checks (what CI runs): `make check`
