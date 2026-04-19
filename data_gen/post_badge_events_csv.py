#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List

SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read badge events from CSV and POST them to an ingest endpoint."
    )
    parser.add_argument(
        "--csv-file",
        default="hospital_badge_events_24h.csv",
        help="Input CSV path. Default: hospital_badge_events_24h.csv",
    )
    parser.add_argument(
        "--endpoint",
        default="http://localhost:8000/api/demo/inject",
        help="Destination endpoint. Default: http://localhost/api/demo/inject",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=10.0,
        help="HTTP timeout per request. Default: 10",
    )
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Exit immediately on the first failed POST.",
    )
    parser.add_argument(
        "--interval-seconds",
        type=float,
        default=5.0,
        help="Delay between POSTs in seconds. Default: 5",
    )
    return parser.parse_args()


def load_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def post_json(endpoint: str, payload: Dict[str, str], timeout_seconds: float) -> tuple[int, str]:
    data = json.dumps(payload).encode("utf-8")
    print(f'data-ilya: {data}')
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        body = response.read().decode("utf-8", errors="replace").strip()
        return response.status, body


def upload_rows(
    rows: Iterable[Dict[str, str]],
    endpoint: str,
    timeout_seconds: float,
    stop_on_error: bool,
    interval_seconds: float,
) -> int:
    success_count = 0
    failure_count = 0

    for index, row in enumerate(rows, start=1):
        try:
            status_code, response_body = post_json(endpoint, row, timeout_seconds)
            print(f"[{index}] POST {status_code} {row.get('timestamp', '')} {row.get('staff_id', '')}")
            if response_body:
                print(f"    {response_body[:300]}")
            success_count += 1
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace").strip()
            print(
                f"[{index}] HTTP {exc.code} for staff_id={row.get('staff_id', '')} timestamp={row.get('timestamp', '')}",
                file=sys.stderr,
            )
            if body:
                print(f"    {body[:300]}", file=sys.stderr)
            failure_count += 1
            if stop_on_error:
                break
        except urllib.error.URLError as exc:
            print(
                f"[{index}] Network error for staff_id={row.get('staff_id', '')} timestamp={row.get('timestamp', '')}: {exc}",
                file=sys.stderr,
            )
            failure_count += 1
            if stop_on_error:
                break

        if index > 0 and interval_seconds > 0:
            time.sleep(interval_seconds)

    print(f"Uploaded: {success_count}, Failed: {failure_count}")
    return 0 if failure_count == 0 else 1


def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv_file)
    if not csv_path.is_absolute():
        candidate = SCRIPT_DIR / csv_path
        if candidate.exists():
            csv_path = candidate
    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}", file=sys.stderr)
        return 1

    rows = load_rows(csv_path)
    if not rows:
        print(f"Error: No rows found in {csv_path}", file=sys.stderr)
        return 1

    return upload_rows(
        rows=rows,
        endpoint=args.endpoint,
        timeout_seconds=args.timeout_seconds,
        stop_on_error=args.stop_on_error,
        interval_seconds=max(args.interval_seconds, 0.0),
    )


if __name__ == "__main__":
    raise SystemExit(main())
