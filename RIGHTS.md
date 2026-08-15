# Dataset provenance and reuse status

**Inventory date:** 2026-08-12; implementation facts reverified 2026-08-15
**Status:** Containment complete; provenance and reuse terms remain under
owner-gated qualified review

This document is the canonical field-level provenance inventory and reuse
notice for HealthArchive dataset releases. It records how fields enter the
exports; it does not decide whether any field is protected, exempt, permitted
by a source term, or otherwise reusable in a particular context.

No blanket reuse licence is currently granted by this repository for the
dataset releases or their contents. Public access, checksums, citation metadata,
and a request to cite a release do not themselves state a reuse permission.
Existing releases remain available and are treated as immutable while the
provenance and reuse review is pending.

## Provenance categories

- **Project metadata** is recorded or authored by HealthArchive to describe its
  capture, processing, or release operations.
- **Source-derived metadata** is observed or extracted from a captured source,
  including URLs, HTTP metadata, language detection, and page titles.
- **Generated identifier or analysis** is assigned or computed by
  HealthArchive from archive records or comparisons.
- **Source name or mark** identifies an originating organization. Names,
  acronyms, domains, and other source-identifying material may also appear in
  source codes and URLs. Their inclusion identifies provenance and does not
  imply affiliation or endorsement.

These categories describe origin, not ownership or permission.

## Snapshot export

Current endpoint: `/api/exports/snapshots`

| Field | Provenance category | What the field records |
|---|---|---|
| `snapshot_id` | Generated identifier or analysis | Numeric identifier assigned to the HealthArchive snapshot record. |
| `source_code` | Project metadata; may reference a source name or mark | Short source identifier assigned by HealthArchive; values may use a source acronym or abbreviation. |
| `source_name` | Source name or mark | Human-readable name of the organization or source being archived. |
| `captured_url` | Source-derived metadata | Source URL requested at capture time; its domain or path may contain source-identifying material. |
| `normalized_url_group` | Generated identifier or analysis | HealthArchive grouping key derived to associate captures of the same page. |
| `capture_timestamp_utc` | Project metadata | UTC time recorded for the capture. |
| `language` | Source-derived metadata | Detected language of captured material, when available. |
| `status_code` | Source-derived metadata | HTTP status observed during capture, when available. |
| `mime_type` | Source-derived metadata | Content type observed during capture, when available. |
| `title` | Source-derived metadata | Extracted page title, when available; this is a limited source-derived text field, not a page body. |
| `capture_backend` | Project metadata | Capture-system label read from the archive job's execution policy when a snapshot is indexed, normalized to lowercase, and defaulted to `browsertrix` when unavailable. |
| `capture_fidelity` | Generated identifier or analysis | Deterministic label derived from `capture_backend`: `browsertrix` maps to `high`; `playwright_warc` and `http_warc` map to `fallback`; any other value maps to `unknown`. This describes the capture path, not a measured per-page quality score or independent validation. |
| `job_id` | Generated identifier or analysis | Numeric identifier for the HealthArchive archive job or edition, when available. |
| `job_name` | Project metadata | HealthArchive-authored archive job or edition label, when available. |
| `snapshot_url` | Generated identifier or analysis | Stable HealthArchive URL generated for the snapshot detail page. |

## Change export

Current endpoint: `/api/exports/changes`

| Field | Provenance category | What the field records |
|---|---|---|
| `change_id` | Generated identifier or analysis | Numeric identifier assigned to the HealthArchive change record. |
| `source_code` | Project metadata; may reference a source name or mark | Short source identifier assigned by HealthArchive; values may use a source acronym or abbreviation. |
| `source_name` | Source name or mark | Human-readable name of the organization or source being archived. |
| `normalized_url_group` | Generated identifier or analysis | HealthArchive grouping key for the page being compared. |
| `from_snapshot_id` | Generated identifier or analysis | Identifier of the earlier HealthArchive snapshot, or null for an initial capture. |
| `to_snapshot_id` | Generated identifier or analysis | Identifier of the later HealthArchive snapshot. |
| `from_capture_timestamp_utc` | Project metadata | UTC capture time of the earlier snapshot, when present. |
| `to_capture_timestamp_utc` | Project metadata | UTC capture time of the later snapshot. |
| `from_job_id` | Generated identifier or analysis | HealthArchive job or edition identifier for the earlier snapshot, when available. |
| `to_job_id` | Generated identifier or analysis | HealthArchive job or edition identifier for the later snapshot, when available. |
| `change_type` | Generated identifier or analysis | HealthArchive-generated change classification, such as a new, updated, removed, or unchanged page. |
| `summary` | Generated identifier or analysis | HealthArchive-generated descriptive summary; it is not a full diff body or source interpretation. |
| `added_sections` | Generated identifier or analysis | Computed count of added sections, when available. |
| `removed_sections` | Generated identifier or analysis | Computed count of removed sections, when available. |
| `changed_sections` | Generated identifier or analysis | Computed count of changed sections, when available. |
| `added_lines` | Generated identifier or analysis | Computed count of added lines, when available. |
| `removed_lines` | Generated identifier or analysis | Computed count of removed lines, when available. |
| `change_ratio` | Generated identifier or analysis | Computed proportional-change score, when available. |
| `high_noise` | Generated identifier or analysis | Computed flag indicating likely layout or boilerplate noise. |
| `diff_truncated` | Generated identifier or analysis | Project-generated flag recording whether the stored diff was truncated. |
| `diff_version` | Project metadata | Identifier of the HealthArchive diff-processing version, when available. |
| `normalization_version` | Project metadata | Identifier of the HealthArchive normalization version, when available. |
| `computed_at_utc` | Project metadata | UTC time when HealthArchive computed the change record. |
| `compare_url` | Generated identifier or analysis | Stable HealthArchive URL generated for the comparison view. |

## Release-wrapper fields

The release tooling copies snapshot and change rows from the public endpoints
without changing their fields after requiring the exact reviewed field sets
documented above. It also creates the following project metadata:

| Field or object | Provenance category | What it records |
|---|---|---|
| `version` | Project metadata | Release-manifest schema version. |
| `tag` | Project metadata | Maintainer-supplied release tag. |
| `releasedAtUtc` | Project metadata | UTC bundle-build time. |
| `apiBase` | Project metadata | API base URL used to build the bundle. |
| `sourceProjectUrl` | Project metadata | HealthArchive project URL. |
| `exportsManifest` | Project metadata | API export-capability response copied at build time. The current response contains `enabled`, `formats`, `defaultLimit`, `maxLimit`, `dataDictionaryUrl`, and per-export `path`, `description`, and `formats` values. |
| `artifacts.snapshots` / `artifacts.changes` | Project metadata; generated identifiers or analysis | For each artifact: `path`, `idField`, `rows`, `minId`, `maxId`, `limitPerRequest`, `requestsMade`, `truncated`, `filename`, and `sha256`. |
| `notes` | Project metadata | Project-authored boundary flags: `metadataOnly`, `noRawHtml`, `noDiffBodies`, `notMedicalAdvice`, and `notCurrentGuidance`. |
| `SHA256SUMS` | Generated identifier or analysis | Generated SHA-256 checksums for the two exports and `manifest.json`. |

## Boundary and known review items

The current contract contains no raw HTML, full page body, WARC payload, replay
asset, full diff body, or diff text. The source-derived text surface is limited
to extracted page titles; change summaries are generated by HealthArchive.

The following rights questions remain open and require qualified review before
another release is approved:

- Source-specific terms and the appropriate treatment of source-derived titles,
  URLs, organization names, acronyms, and other marks.
- The scope, if any, of a future licence for project-created metadata and code,
  considered separately from source-derived and source-identifying fields.
- Whether the deterministic `capture_fidelity` terminology needs a clearer
  consumer-facing qualifier even though its generation rule is now documented.

The earlier CC BY 4.0 structured-data inconsistency is no longer an open
implementation defect. The coordinated application correction removed that
blanket licence signal, published the current English/French dictionaries, and
linked this notice in monorepo merge
`443edd97278cf0c21bb525f24696dce2ddb61cad`; frontend release
`ac4e88cb1775` was then verified live. That correction did not decide the open
rights questions above or grant a licence.

If the export schema changes, this inventory must be updated before the changed
surface is included in a newly approved release.

## Owner-gated qualified review packet

**Packet status:** prepared; no external contact is authorized.

The smallest review surface is:

1. this 39-field provenance inventory and conservative reuse notice;
2. the current 15-field snapshot and 24-field change schema in
   `scripts/export_schema.py`;
3. the existing `healtharchive-dataset-2026-07-01` metadata-only release and
   its manifest/checksums; and
4. the English/French data dictionaries linked from the HealthArchive exports
   page.

The exact request to one named institutional librarian, copyright/reuse
specialist, or comparably qualified reviewer is:

> Please review only the attached HealthArchive metadata-release provenance
> inventory and conservative notice. For each field category, identify any
> source-specific terms, attribution or notice requirements, mark-related
> concerns, or other concrete barrier that should be addressed before another
> metadata release. Please also say whether project-created metadata could be
> given separate reuse terms without implying permission for source-derived
> fields, whether the `capture_fidelity` explanation needs correction, and
> whether the existing July 2026 release requires a specific notice or access
> change. A short written issue list with source links, explicit unknowns, and
> recommended wording is sufficient; this request does not ask for a blanket
> legal conclusion, publication endorsement, or research collaboration.

Before sending that request, the maintainer must record the named reviewer,
why their role is qualified, the exact written output, a numeric workload cap,
and approval to contact them. One contact is stewardship; it must not become an
outreach campaign.

Stop without expanding the task if no suitable reviewer is available, the
review cannot fit its approved cap, or the reviewer says a broader legal
analysis is required. A no-red-flag or no-response outcome does not select a
licence, approve a release, or establish permission. Publication stays paused
until a separate maintainer decision addresses the written review outcome,
schema, continuity posture, and release approval together.
