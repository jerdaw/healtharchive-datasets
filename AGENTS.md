# AGENTS.md – HealthArchive datasets

## Project overview

- This repo publishes **versioned, citable dataset releases** for HealthArchive as **metadata-only** exports.
- Releases are produced by GitHub Actions by calling the public export endpoints and validating checksums/invariants.
- Goal: reproducibility + auditability (treat releases as immutable research objects).

Primary docs to consult first:

- `README.md` – release contents and integrity rules.
- `DOCUMENTATION.md` – documentation boundaries + linking rules.
- Backend docs site (MkDocs): https://docs.healtharchive.ca (built from the backend repo)
- Canonical documentation guidelines: https://docs.healtharchive.ca/documentation-guidelines/
- Export integrity contract: https://github.com/jerdaw/healtharchive-backend/blob/main/docs/operations/export-integrity-contract.md
- Dataset release runbook: https://github.com/jerdaw/healtharchive-backend/blob/main/docs/operations/dataset-release-runbook.md

---

## Dev environment & commands

From the repo root:

- Create venv: `make venv`
- Full checks (what CI runs): `make check`

---

## Git workflow (commits & pushes)

Default for agentic work: **do not commit or push** unless the human operator explicitly asks.

If asked to commit:

- Prefer small, logically grouped commits.
- Run `make check` before pushing.
- Never commit secrets, `.env` files, tokens, or machine-local artifacts.

## Attribution and compatibility policy

- All git author metadata must stay human-only. Do not use assistant, bot, or
  automation identities (for example: Codex, Claude, Gemini, Copilot,
  ChatGPT, `dependabot[bot]`, or `CI User`) in author fields or
  `Co-Authored-By` trailers.
- Do not add non-human contributor or authorship credit in docs, changelogs,
  workflow notes, or release metadata.
- If a dependency bump or other automated suggestion is accepted, land it as a
  new human-authored commit instead of merging bot-authored history directly.
- `CLAUDE.md` and `GEMINI.md` are compatibility symlinks to `AGENTS.md` only;
  they are not contributor identities.
---

## Safety rails / things not to touch casually

- Do not change tag/immutability rules without updating docs and making it explicit in release notes.
- Do not weaken checksum/manifest validation.
- Keep everything public-safe: no secrets, private emails, or internal hostnames in docs or workflow logs.
