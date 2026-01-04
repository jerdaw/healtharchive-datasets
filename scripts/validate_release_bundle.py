from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Artifact:
    name: str
    filename: str
    sha256: str
    rows: int
    min_id: int | None
    max_id: int | None
    requests_made: int
    limit_per_request: int
    truncated: bool


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _require(obj: dict[str, Any], key: str) -> Any:
    if key not in obj:
        raise ValueError(f"manifest missing required field: {key}")
    return obj[key]


def _require_dict(obj: dict[str, Any], key: str) -> dict[str, Any]:
    value = _require(obj, key)
    if not isinstance(value, dict):
        raise ValueError(f"manifest field {key!r} must be an object")
    return value


def _parse_artifact(meta: dict[str, Any], name: str) -> Artifact:
    def req_str(k: str) -> str:
        v = _require(meta, k)
        if not isinstance(v, str) or not v.strip():
            raise ValueError(f"artifacts.{name}.{k} must be a non-empty string")
        return v.strip()

    def req_int(k: str) -> int:
        v = _require(meta, k)
        if not isinstance(v, int):
            raise ValueError(f"artifacts.{name}.{k} must be an integer")
        return v

    def opt_int(k: str) -> int | None:
        v = meta.get(k)
        if v is None:
            return None
        if not isinstance(v, int):
            raise ValueError(f"artifacts.{name}.{k} must be an integer or null")
        return v

    def req_bool(k: str) -> bool:
        v = _require(meta, k)
        if not isinstance(v, bool):
            raise ValueError(f"artifacts.{name}.{k} must be a boolean")
        return v

    filename = req_str("filename")
    sha256 = req_str("sha256")
    rows = req_int("rows")
    min_id = opt_int("minId")
    max_id = opt_int("maxId")
    requests_made = req_int("requestsMade")
    limit_per_request = req_int("limitPerRequest")
    truncated = req_bool("truncated")

    if rows < 0:
        raise ValueError(f"artifacts.{name}.rows must be >= 0")

    if rows == 0:
        if min_id is not None or max_id is not None:
            raise ValueError(
                f"artifacts.{name} has rows=0 but minId/maxId are not null (minId={min_id}, maxId={max_id})"
            )
    else:
        if min_id is None or max_id is None:
            raise ValueError(f"artifacts.{name} has rows>0 but minId/maxId are null")
        if min_id > max_id:
            raise ValueError(f"artifacts.{name}.minId must be <= maxId")
        if requests_made < 1:
            raise ValueError(f"artifacts.{name}.requestsMade must be >= 1 when rows>0")

    if limit_per_request <= 0:
        raise ValueError(f"artifacts.{name}.limitPerRequest must be > 0")

    if requests_made <= 0:
        raise ValueError(f"artifacts.{name}.requestsMade must be > 0")

    return Artifact(
        name=name,
        filename=filename,
        sha256=sha256,
        rows=rows,
        min_id=min_id,
        max_id=max_id,
        requests_made=requests_made,
        limit_per_request=limit_per_request,
        truncated=truncated,
    )


def _validate_sha256sums(bundle_dir: Path, sums_path: Path) -> None:
    expected: dict[str, str] = {}
    for raw in sums_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid SHA256SUMS line: {raw!r}")
        sha = parts[0].strip()
        filename = parts[-1].strip()
        expected[filename] = sha

    if not expected:
        raise ValueError("SHA256SUMS is empty")

    for filename, sha in expected.items():
        path = bundle_dir / filename
        if not path.exists():
            raise ValueError(f"SHA256SUMS references missing file: {filename}")
        actual = _sha256_file(path)
        if actual != sha:
            raise ValueError(f"SHA256 mismatch for {filename}: expected {sha} got {actual}")


def _validate_gzip(path: Path) -> None:
    try:
        with gzip.open(path, "rb") as gz:
            for _ in gz:
                pass
    except Exception as exc:  # noqa: BLE001 - validation wants context
        raise ValueError(f"gzip integrity check failed for {path.name}: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a HealthArchive datasets release bundle (manifest + SHA256SUMS + artifacts)."
    )
    parser.add_argument(
        "--bundle-dir",
        default="dist",
        help="Directory containing manifest.json, SHA256SUMS, and release artifacts.",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Allow rows=0 (normally treated as suspicious and invalid).",
    )
    parser.add_argument(
        "--allow-truncated",
        action="store_true",
        help="Allow truncated=true (for local smoke tests only; publish workflow forbids truncated bundles).",
    )
    args = parser.parse_args()

    bundle_dir = Path(args.bundle_dir)
    manifest_path = bundle_dir / "manifest.json"
    sums_path = bundle_dir / "SHA256SUMS"

    if not manifest_path.exists():
        raise SystemExit(f"ERROR: Missing manifest.json at {manifest_path}")
    if not sums_path.exists():
        raise SystemExit(f"ERROR: Missing SHA256SUMS at {sums_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise SystemExit("ERROR: manifest.json must contain a JSON object")

    version = _require(manifest, "version")
    if not isinstance(version, int) or version <= 0:
        raise SystemExit("ERROR: manifest.version must be a positive integer")

    for required in ("tag", "releasedAtUtc", "apiBase"):
        value = _require(manifest, required)
        if not isinstance(value, str) or not value.strip():
            raise SystemExit(f"ERROR: manifest.{required} must be a non-empty string")

    exports_manifest = _require(manifest, "exportsManifest")
    if not isinstance(exports_manifest, dict):
        raise SystemExit("ERROR: manifest.exportsManifest must be an object")
    if "enabled" not in exports_manifest:
        raise SystemExit(
            "ERROR: exportsManifest.enabled missing (expected API /api/exports payload)"
        )

    artifacts = _require_dict(manifest, "artifacts")
    snapshots = _require_dict(artifacts, "snapshots")
    changes = _require_dict(artifacts, "changes")

    snapshots_artifact = _parse_artifact(snapshots, "snapshots")
    changes_artifact = _parse_artifact(changes, "changes")

    if not args.allow_truncated and (snapshots_artifact.truncated or changes_artifact.truncated):
        raise SystemExit(
            "ERROR: truncated release is not publishable "
            f"(snapshots.truncated={snapshots_artifact.truncated}, changes.truncated={changes_artifact.truncated}). "
            "Re-run with --allow-truncated for local smoke tests."
        )

    if not args.allow_empty and (snapshots_artifact.rows == 0 or changes_artifact.rows == 0):
        raise SystemExit(
            f"ERROR: rows=0 is suspicious; aborting (snapshots.rows={snapshots_artifact.rows}, changes.rows={changes_artifact.rows}). Re-run with --allow-empty to override."
        )

    # Validate artifacts exist and match the manifest sha256.
    for artifact in (snapshots_artifact, changes_artifact):
        path = bundle_dir / artifact.filename
        if not path.exists():
            raise SystemExit(f"ERROR: Missing artifact file: {artifact.filename}")
        actual = _sha256_file(path)
        if actual != artifact.sha256:
            raise SystemExit(
                f"ERROR: manifest sha256 mismatch for {artifact.filename}: expected {artifact.sha256} got {actual}"
            )
        if artifact.filename.endswith(".gz"):
            _validate_gzip(path)

    # Validate manifest.json is itself checksummed correctly by SHA256SUMS and that all checksums match.
    _validate_sha256sums(bundle_dir, sums_path)

    print("OK: release bundle validated")
    print(f"- tag: {manifest['tag']}")
    print(f"- apiBase: {manifest['apiBase']}")
    print(
        f"- snapshots: {snapshots_artifact.rows} rows (minId={snapshots_artifact.min_id}, maxId={snapshots_artifact.max_id})"
    )
    print(
        f"- changes: {changes_artifact.rows} rows (minId={changes_artifact.min_id}, maxId={changes_artifact.max_id})"
    )
    if snapshots_artifact.truncated or changes_artifact.truncated:
        print(
            f"WARNING: truncated=true (snapshots={snapshots_artifact.truncated}, changes={changes_artifact.truncated})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
