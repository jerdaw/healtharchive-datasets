# Contributing (HealthArchive Datasets)

## Quickstart

- Create venv: `make venv`
- Full checks (what CI runs): `make check`

## Optional: pre-commit

This repo includes a `.pre-commit-config.yaml` with fast, mechanical checks (whitespace/EOF, YAML/TOML validation, detecting private keys).

- Install (recommended): `python -m pip install --user pre-commit`
- Enable: `pre-commit install`
- Run on demand: `pre-commit run --all-files`

## Optional: pre-push (recommended for solo-fast direct-to-main)

If you're pushing directly to `main`, a local pre-push hook helps keep "green main" true by running `make check` before every push.

- Install: `./scripts/install-pre-push-hook.sh`
- Bypass once: `git push --no-verify` (or set `HA_SKIP_PRE_PUSH=1`)

## Documentation guidelines

- Follow `DOCUMENTATION.md` (this repo) and the canonical cross-repo guidelines at https://docs.healtharchive.ca/documentation-guidelines/
