# HealthArchive Datasets Roadmap

**Current state:** Stable metadata-only quarterly release pipeline
**Last updated:** 2026-07-13
**Repository-only execution queue:** empty unless a release-integrity,
security, dependency, or documentation regression appears

## Priority order

| Priority | Outcome | Readiness | Gate / next action |
|----------|---------|-----------|--------------------|
| P0 | Select and add a repository license | Human/legal decision | A maintainer chooses the license; then add the canonical file and synchronize README, citation, release, and package metadata |
| P0 | Keep quarterly releases reproducible and immutable | Standing maintenance | Act on a failed scheduled release, checksum/manifest regression, public export contract change, or security advisory |
| P1 | Publish the first DOI-backed formal dataset release | External/release intent | Approve publication, choose the release date and DOI workflow, run the validated export, and record the citation artifact |
| P1 | Preserve cross-repository export compatibility | Conditional | Update this repository only when the HealthArchive public export contract changes |
| P2 | Improve adoption and citation evidence | External/human | Add only real public citations, releases, and permission-aware adoption signals |

## Selection rules

1. Do not publish, retag, replace, or mutate a release without explicit release
   intent.
2. Do not choose a license automatically.
3. Keep this repository metadata-only; raw HTML, WARC files, full page bodies,
   and full diff bodies remain out of scope.
4. Prefer small integrity and reproducibility fixes over expanding the dataset
   surface.

## Completed foundation

- Quarterly and manually dispatched GitHub release workflow
- Paginated public snapshots and changes export ingestion
- Gzipped JSONL artifacts, manifest invariants, and SHA-256 verification
- Immutable date-based release tags and bounded recovery guidance
- Citation metadata, security policy, issue forms, and documentation checks

## External dependencies

- HealthArchive public export availability and contract stability
- Human release and DOI publication intent
- Human/legal license selection
- Real public citation or adoption evidence

The application-level archive, integrity generator, and broader research
roadmap remain in the main HealthArchive repository. This file owns only the
dataset-release repository's active priorities and gates.
