# Documentation guidelines (datasets)

This repo publishes versioned, citable **metadata-only** dataset releases for
public-interest archival, research, and monitoring use.

## Canonical docs model

- Dataset release documentation is canonical in this repo (primarily `README.md` and release workflow docs).
- Backend ops/runbooks live in the backend docs portal: https://docs.healtharchive.ca
- Export integrity contract: https://github.com/jerdaw/healtharchive/blob/main/docs/operations/export-integrity-contract.md
- Dataset release runbook: https://github.com/jerdaw/healtharchive/blob/main/docs/operations/dataset-release-runbook.md
- Canonical cross-repo documentation guidelines: https://docs.healtharchive.ca/documentation-guidelines/
- Canonical roadmap process: https://github.com/jerdaw/healtharchive/blob/main/docs/roadmap-process.md
- Canonical backlog for cross-repo work: https://github.com/jerdaw/healtharchive/blob/main/docs/planning/roadmap.md

## Cross-repo boundaries (avoid drift)

- Prefer pointers (links) over copying prose between repos.
- When referencing backend or frontend docs, prefer GitHub or `docs.healtharchive.ca` links over local workspace-relative paths.
- Keep everything public-safe (no secrets, private emails, internal hostnames/IPs).

## Public documentation boundary

- Dataset docs may describe schema, release validation, checksum verification,
  limitations, and safe local development workflows.
- Do not copy raw scraped content, full HTML/page bodies, backend deployment
  runbooks, credentials, private hostnames/IPs, or environment-specific paths
  into this repo.
- This repo does not maintain a separate local roadmap or decision-record
  archive. Track cross-repo backlog and process items in the backend docs, and
  add local decision records only if a dataset-release-specific architectural
  decision needs a canonical record here.
