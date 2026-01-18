# Documentation guidelines (datasets)

This repo publishes versioned, citable **metadata-only** dataset releases.

## Canonical docs model

- Dataset release documentation is canonical in this repo (primarily `README.md` and release workflow docs).
- Backend ops/runbooks live in the backend docs portal: https://docs.healtharchive.ca
- Cross-repo environment wiring (canonical): https://docs.healtharchive.ca/deployment/environments-and-configuration/
- Canonical cross-repo documentation guidelines: https://docs.healtharchive.ca/documentation-guidelines/

## Cross-repo boundaries (avoid drift)

- Prefer pointers (links) over copying prose between repos.
- When referencing backend or frontend docs, prefer GitHub or `docs.healtharchive.ca` links over local workspace-relative paths.
- Keep everything public-safe (no secrets, private emails, internal hostnames/IPs).
