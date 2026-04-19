#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT = SCRIPT_DIR / "suspicious_person_reports_24h.csv"
REPORTERS = ["security", "medical staff", "custodial staff", "visitor", "patient"]
LOCATIONS = [
    "Imaging Service Corridor",
    "Emergency Department Ambulance Bay",
    "South Service Entrance",
    "Pharmacy Hallway",
    "Labor and Delivery Waiting Area",
    "Main Lobby",
    "Sterile Processing Corridor",
    "ICU Family Lounge",
]
DESCRIPTION_TEMPLATES = [
    "Unknown person seen lingering near {location} and repeatedly looking into staff-only rooms.",
    "Individual without visible badge attempted to follow staff through a secured door near {location}.",
    "Person in mismatched scrubs observed pushing unattended equipment cases toward {location}.",
    "Unidentified person photographed badge readers and access panels near {location}.",
    "Individual loitered near {location} and tried multiple locked doors before walking away.",
    "Person claiming to look for a relative entered a restricted hallway near {location} without authorization.",
    "Unknown person was seen moving a supply cart through {location} and could not explain where it came from.",
    "Agitated individual paced near {location}, questioned staff about medications, and refused to leave the area.",
    "Person without patient wristband entered {location} and attempted to open a staff equipment cabinet.",
    "Visitor was reported watching shift change activity near {location} and recording on a phone.",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate suspicious-person report CSV rows for hospital scenarios."
    )
    parser.add_argument(
        "--output-file",
        default=str(DEFAULT_OUTPUT),
        help=f"Output CSV path. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=20,
        help="Number of rows to generate. Default: 20",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for deterministic output. Default: 42",
    )
    parser.add_argument(
        "--start-time",
        default=None,
        help="Start time in ISO format. Default: current UTC time minus 24 hours",
    )
    parser.add_argument(
        "--interval-minutes",
        type=int,
        default=30,
        help="Base interval between reports in minutes. Default: 30",
    )
    return parser.parse_args()


def parse_start_time(raw_value: str | None) -> datetime:
    if raw_value:
        normalized = raw_value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).astimezone(timezone.utc)
    return datetime.now(timezone.utc) - timedelta(hours=24)


def to_iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def build_row(index: int, occurred_at: datetime, rng: random.Random) -> dict[str, str]:
    location = rng.choice(LOCATIONS)
    verified = rng.choices(["yes", "no"], weights=[7, 3], k=1)[0]
    removed = rng.choices(["yes", "no"], weights=[3, 7], k=1)[0]
    if verified == "no" and removed == "yes":
        removed = "no"

    return {
        "report_id": f"SPR-{index:04d}",
        "occurred_at": to_iso_z(occurred_at),
        "reporter": rng.choice(REPORTERS),
        "location": location,
        "description": rng.choice(DESCRIPTION_TEMPLATES).format(location=location),
        "verified": verified,
        "person_removed": removed,
    }


def generate_rows(
    count: int,
    start_time: datetime,
    interval_minutes: int,
    rng: random.Random,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current_time = start_time

    for index in range(1, count + 1):
        current_time += timedelta(minutes=max(interval_minutes, 1) + rng.randint(0, 12))
        rows.append(build_row(index=index, occurred_at=current_time, rng=rng))

    return rows


def write_rows(output_file: Path, rows: list[dict[str, str]]) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "report_id",
                "occurred_at",
                "reporter",
                "location",
                "description",
                "verified",
                "person_removed",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    rng = random.Random(args.seed)
    rows = generate_rows(
        count=max(args.count, 0),
        start_time=parse_start_time(args.start_time),
        interval_minutes=args.interval_minutes,
        rng=rng,
    )
    write_rows(Path(args.output_file), rows)
    print(f"Wrote {len(rows)} rows to {args.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
