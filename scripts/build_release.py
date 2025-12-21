from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import socket
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _http_json(url: str, *, timeout: float, user_agent: str, retries: int = 4) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": user_agent,
        },
    )
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"GET {url} failed with HTTP {resp.status}")
                payload = resp.read()
                return json.loads(payload.decode("utf-8"))
        except Exception as exc:
            last_exc = exc
            if attempt >= retries:
                break
            time.sleep(1.5**attempt)
    raise RuntimeError(f"Failed to fetch JSON from {url}: {last_exc}")


def _http_ndjson_stream(url: str, *, timeout: float, user_agent: str, retries: int = 4):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/x-ndjson",
            "User-Agent": user_agent,
        },
    )
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            resp = urllib.request.urlopen(req, timeout=timeout)
            if resp.status != 200:
                body = resp.read(2048)
                raise RuntimeError(
                    f"GET {url} failed with HTTP {resp.status}: {body.decode('utf-8', errors='replace')}"
                )
            return resp
        except Exception as exc:
            last_exc = exc
            if attempt >= retries:
                break
            time.sleep(1.5**attempt)
    raise RuntimeError(f"Failed to stream NDJSON from {url}: {last_exc}")


def _download_export_to_gzip_jsonl(
    *,
    api_base: str,
    path: str,
    id_field: str,
    out_path: Path,
    limit: int,
    timeout: float,
    user_agent: str,
) -> dict[str, Any]:
    after_id: int | None = None
    rows = 0
    min_id: int | None = None
    max_id: int | None = None
    requests_made = 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(out_path, "wb", compresslevel=6, mtime=0) as gz:
        while True:
            params = {
                "format": "jsonl",
                "compressed": "false",
                "limit": str(limit),
            }
            if after_id is not None:
                params["afterId"] = str(after_id)
            url = f"{api_base}{path}?{urllib.parse.urlencode(params)}"

            resp = _http_ndjson_stream(url, timeout=timeout, user_agent=user_agent)
            page_rows = 0
            last_id: int | None = None
            try:
                for raw_line in resp:
                    if not raw_line.strip():
                        continue
                    page_rows += 1
                    rows += 1
                    if raw_line.endswith(b"\n"):
                        line = raw_line
                    else:
                        line = raw_line + b"\n"
                    obj = json.loads(line.decode("utf-8"))
                    value = obj.get(id_field)
                    if isinstance(value, int):
                        last_id = value
                        if min_id is None:
                            min_id = value
                        max_id = value
                    gz.write(line)
            finally:
                resp.close()

            requests_made += 1
            if page_rows == 0:
                break
            if last_id is None:
                raise RuntimeError(f"Export {path} returned rows without '{id_field}'")
            if after_id is not None and last_id <= after_id:
                raise RuntimeError(
                    f"Pagination did not advance for {path}: afterId={after_id} lastId={last_id}"
                )
            after_id = last_id

    return {
        "path": path,
        "idField": id_field,
        "rows": rows,
        "minId": min_id,
        "maxId": max_id,
        "limitPerRequest": limit,
        "requestsMade": requests_made,
        "filename": out_path.name,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a HealthArchive dataset release bundle.")
    parser.add_argument("--api-base", default="https://api.healtharchive.ca", help="API host base URL.")
    parser.add_argument("--out-dir", default="dist", help="Output directory for release files.")
    parser.add_argument("--tag", required=True, help="Release tag (e.g., healtharchive-dataset-YYYY-MM-DD).")
    parser.add_argument("--timeout-seconds", type=float, default=60.0, help="HTTP timeout per request.")
    parser.add_argument("--limit", type=int, default=10000, help="Rows per request (paginates via afterId).")
    args = parser.parse_args()

    socket.setdefaulttimeout(args.timeout_seconds)

    api_base = str(args.api_base).rstrip("/")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    user_agent = f"healtharchive-datasets/1.0 (+{api_base})"

    exports_manifest = _http_json(
        f"{api_base}/api/exports", timeout=args.timeout_seconds, user_agent=user_agent
    )
    if not exports_manifest.get("enabled"):
        raise RuntimeError("Exports are disabled on the API; cannot build a dataset release.")

    max_limit = int(exports_manifest.get("maxLimit") or args.limit)
    limit = min(int(args.limit), max_limit)

    snapshots_path = out_dir / "healtharchive-snapshots.jsonl.gz"
    changes_path = out_dir / "healtharchive-changes.jsonl.gz"

    snapshots_meta = _download_export_to_gzip_jsonl(
        api_base=api_base,
        path="/api/exports/snapshots",
        id_field="snapshot_id",
        out_path=snapshots_path,
        limit=limit,
        timeout=args.timeout_seconds,
        user_agent=user_agent,
    )
    changes_meta = _download_export_to_gzip_jsonl(
        api_base=api_base,
        path="/api/exports/changes",
        id_field="change_id",
        out_path=changes_path,
        limit=limit,
        timeout=args.timeout_seconds,
        user_agent=user_agent,
    )

    snapshots_sha = _sha256_file(snapshots_path)
    changes_sha = _sha256_file(changes_path)

    manifest = {
        "version": 1,
        "tag": args.tag,
        "releasedAtUtc": _utc_now_iso(),
        "apiBase": api_base,
        "sourceProjectUrl": "https://healtharchive.ca",
        "exportsManifest": exports_manifest,
        "artifacts": {
            "snapshots": {**snapshots_meta, "sha256": snapshots_sha},
            "changes": {**changes_meta, "sha256": changes_sha},
        },
        "notes": {
            "metadataOnly": True,
            "noRawHtml": True,
            "noDiffBodies": True,
            "notMedicalAdvice": True,
            "notCurrentGuidance": True,
        },
    }

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_sha = _sha256_file(manifest_path)

    sums_path = out_dir / "SHA256SUMS"
    sums_path.write_text(
        "\n".join(
            [
                f"{snapshots_sha}  {snapshots_path.name}",
                f"{changes_sha}  {changes_path.name}",
                f"{manifest_sha}  {manifest_path.name}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Wrote {snapshots_path} ({snapshots_meta['rows']} rows)")
    print(f"Wrote {changes_path} ({changes_meta['rows']} rows)")
    print(f"Wrote {manifest_path}")
    print(f"Wrote {sums_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
