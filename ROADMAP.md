# HealthArchive Datasets Roadmap

**Current state:** Terminal event-triggered stewardship. Release and claim
containment is complete; new publication remains manually gated and paused
pending reuse and governance review.
**Last updated:** 2026-08-15
**Repository-only execution queue:** no release execution while paused; act only
on an integrity, security, dependency, or documentation regression

## Priority order

| Priority | Outcome | Readiness | Gate / next action |
|----------|---------|-----------|--------------------|
| Gate | Obtain one qualified reuse and governance review | Owner-triggered; packet prepared | `RIGHTS.md` contains the bounded request, but no contact is authorized until the maintainer records a named qualified reviewer, output, numeric workload cap, and approval |
| Event | Keep manual release tooling reproducible and existing releases immutable | Triggered maintenance | Act on a checksum/manifest regression, public export contract change, documentation defect, or security advisory |
| Inactive | Consider a DOI-backed formal dataset release | Later separate decision required | No DOI work is active. Reconsider only after a qualified review and a separate decision define the curation purpose, approved release, workload, and stop rule |
| P1 | Preserve cross-repository export compatibility | Conditional | Update this repository only when the HealthArchive public export contract changes |
| Event | Record independently arising public citation or use evidence | Event-triggered; no campaign | Record only verifiable, permission-aware public evidence when it arises; do not run adoption outreach, download tracking, or periodic follow-up |

## Selection rules

1. Keep new publication paused until the reuse and governance review gate is
   resolved. After that, do not publish, retag, replace, or mutate a release
   without explicit maintainer approval and manual dispatch.
2. Do not choose a license automatically.
3. Keep this repository metadata-only; raw HTML, WARC files, full page bodies,
   and full diff bodies remain out of scope.
4. Prefer small integrity and reproducibility fixes over expanding the dataset
   surface.
5. Do not add scheduled publication or scheduled keepalive triggers.
6. DOI publication and adoption promotion are inactive. Neither is implied by
   completion of the reuse review; each requires a later separate decision.
7. Keep the repository execution queue empty while no event or owner gate has
   changed. A prepared review packet is not authorization to contact anyone.

## Completed foundation

- Manually dispatched GitHub release workflow; scheduled publication and
  keepalive triggers removed on 2026-08-12
- Paginated public snapshots and changes export ingestion
- Gzipped JSONL artifacts, manifest invariants, and SHA-256 verification
- Immutable date-based release tags and bounded recovery guidance
- Citation metadata, security policy, issue forms, and documentation checks

## External dependencies

- HealthArchive public export availability and contract stability
- One owner-approved qualified reuse and governance review, if selected under
  the `RIGHTS.md` gate
- Human release and licensing decisions; a DOI workflow only after a later
  separate decision
- Independently arising public citation or use evidence; no collection cadence
  or outreach campaign

The application-level archive, integrity generator, and broader research
roadmap remain in the main HealthArchive repository. This file owns only the
dataset-release repository's active priorities and gates.
