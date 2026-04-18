#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
import datetime
import random
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def parse_schedule_days(value: str) -> Sequence[str]:
    return [token.strip() for token in value.split(",") if token.strip()]


def parse_time(value: str) -> Optional[datetime.time]:
    value = (value or "").strip()
    if not value or value.lower() == "varies":
        return None
    try:
        return datetime.datetime.strptime(value, "%H:%M").time()
    except ValueError:
        return None


def load_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle)]


def hours_to_time(hours: int, minutes: int = 0) -> datetime.time:
    return datetime.time(hour=hours, minute=minutes)


def default_shift_window(shift_label: str, now: datetime.datetime) -> Tuple[datetime.datetime, datetime.datetime]:
    label = (shift_label or "").strip().lower()
    if "night" in label:
        start = hours_to_time(22)
        end = hours_to_time(7)
    elif "evening" in label:
        start = hours_to_time(15)
        end = hours_to_time(23)
    elif "day" in label:
        start = hours_to_time(7)
        end = hours_to_time(15)
    else:
        start = hours_to_time(8)
        end = hours_to_time(16)

    start_dt = datetime.datetime.combine(now.date(), start)
    end_dt = datetime.datetime.combine(now.date(), end)
    if end_dt <= start_dt:
        end_dt += datetime.timedelta(days=1)
    return start_dt, end_dt


def shift_window_for_staff(staff: Dict[str, str], now: datetime.datetime) -> Optional[Tuple[datetime.datetime, datetime.datetime]]:
    schedule_days = parse_schedule_days(staff.get("schedule_days", ""))
    today_name = DAY_NAMES[now.weekday()]
    if schedule_days and today_name not in schedule_days:
        return None

    start_time = parse_time(staff.get("shift_start", ""))
    end_time = parse_time(staff.get("shift_end", ""))
    if start_time and end_time:
        start_dt = datetime.datetime.combine(now.date(), start_time)
        end_dt = datetime.datetime.combine(now.date(), end_time)
        if end_dt <= start_dt:
            end_dt += datetime.timedelta(days=1)
        return start_dt, end_dt

    return default_shift_window(staff.get("shift", ""), now)


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def door_weight(door: Dict[str, str], staff: Dict[str, str]) -> int:
    weight = 1
    department = normalize_text(staff.get("department", ""))
    role_category = normalize_text(staff.get("role_category", ""))
    door_text = normalize_text(f"{door.get('area', '')} {door.get('door_name', '')}")

    for token in re.findall(r"[A-Za-z0-9]+", department):
        if token and token in door_text:
            weight += 6

    if "clinical" in role_category and any(term in door_text for term in ["nurse", "patient room", "medication", "supply", "icu", "surgical", "emergency", "radiology", "laboratory"]):
        weight += 5
    if "administrative" in role_category and any(term in door_text for term in ["office", "records", "admissions", "billing", "reception"]):
        weight += 4
    if "support" in role_category and any(term in door_text for term in ["service", "supply", "laundry", "transport", "housekeeping", "security"]):
        weight += 4
    if "specialized" in role_category and any(term in door_text for term in ["pharmacy", "quality", "infection", "research", "anesthesia"]):
        weight += 3

    if door.get("category", "").strip().lower() == "perimeter":
        weight += 2
    if door.get("door_type", "").strip().lower() == "perimeter door":
        weight += 2

    return max(weight, 1)


def weighted_choice(items: Sequence[Tuple[Dict[str, str], int]], count: int = 1) -> List[Dict[str, str]]:
    if not items:
        return []
    population, weights = zip(*items)
    if count == 1:
        return [random.choices(population, weights=weights, k=1)[0]]
    return random.choices(population, weights=weights, k=count)


def choose_doors(staff: Dict[str, str], doors: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    return weighted_choice([(door, door_weight(door, staff)) for door in doors], count=min(4, max(1, len(doors))))


def clamp_timestamp(timestamp: datetime.datetime, earliest: datetime.datetime, latest: datetime.datetime) -> datetime.datetime:
    if timestamp < earliest:
        return earliest
    if timestamp > latest:
        return latest
    return timestamp


def build_event_row(staff: Dict[str, str], event_time: datetime.datetime, door: Dict[str, str], action: str) -> Dict[str, str]:
    return {
        "timestamp": event_time.isoformat(sep=" ", timespec="seconds"),
        "staff_id": staff.get("staff_id", ""),
        "first_name": staff.get("first_name", ""),
        "last_name": staff.get("last_name", ""),
        "role_title": staff.get("role_title", ""),
        "role_category": staff.get("role_category", ""),
        "department": staff.get("department", ""),
        "shift": staff.get("shift", ""),
        "door_name": door.get("door_name", ""),
        "category": door.get("category", ""),
        "area": door.get("area", ""),
        "door_type": door.get("door_type", ""),
        "badge_required": door.get("badge_required", ""),
        "action": action,
        "access_result": "Granted",
    }


def generate_badge_events_for_staff(
    staff: Dict[str, str],
    perimeter_doors: Sequence[Dict[str, str]],
    interior_doors: Sequence[Dict[str, str]],
    now: datetime.datetime,
    window_start: datetime.datetime,
    include_off_duty: bool,
) -> List[Dict[str, str]]:
    events: List[Dict[str, str]] = []
    shift_window = shift_window_for_staff(staff, now)
    if shift_window is not None:
        shift_start, shift_end = shift_window
        shift_inside_window = shift_end >= window_start and shift_start <= now
        if shift_inside_window:
            entry_door = random.choice(perimeter_doors)
            entry_time = shift_start + datetime.timedelta(minutes=random.randint(-15, 10))
            entry_time = clamp_timestamp(entry_time, window_start, now)
            if window_start <= entry_time <= now:
                events.append(build_event_row(staff, entry_time, entry_door, "enter"))

            interior_candidates = [(door, door_weight(door, staff)) for door in interior_doors]
            interior_door_count = random.randint(1, 3)
            interior_paths = weighted_choice(interior_candidates, count=interior_door_count)
            for idx, door in enumerate(interior_paths, start=1):
                interior_time = shift_start + datetime.timedelta(minutes=20 + idx * random.randint(15, 40))
                interior_time = clamp_timestamp(interior_time, window_start, now)
                if window_start <= interior_time <= now:
                    events.append(build_event_row(staff, interior_time, door, "enter"))

            exit_time = shift_end + datetime.timedelta(minutes=random.randint(-10, 15))
            exit_time = clamp_timestamp(exit_time, window_start, now)
            if window_start <= exit_time <= now:
                exit_door = random.choice(perimeter_doors)
                events.append(build_event_row(staff, exit_time, exit_door, "exit"))

    if include_off_duty and random.random() < 0.04:
        off_duty_time = window_start + datetime.timedelta(seconds=random.randint(0, int((now - window_start).total_seconds())))
        door = random.choice(perimeter_doors)
        action = random.choice(["enter", "exit"])
        events.append(build_event_row(staff, off_duty_time, door, action))

    return sorted(events, key=lambda row: row["timestamp"])


def generate_badging_history(
    staff_rows: Sequence[Dict[str, str]],
    doors_rows: Sequence[Dict[str, str]],
    now: datetime.datetime,
    include_off_duty: bool,
    max_staff: Optional[int] = None,
) -> List[Dict[str, str]]:
    badge_doors = [door for door in doors_rows if normalize_text(door.get("badge_required", "")) == "yes"]
    perimeter_doors = [door for door in badge_doors if normalize_text(door.get("door_type", "")) == "perimeter door"]
    interior_doors = [door for door in badge_doors if normalize_text(door.get("door_type", "")) != "perimeter door"]
    if not perimeter_doors:
        raise ValueError("No perimeter doors found in door dataset.")
    if not interior_doors:
        interior_doors = badge_doors

    if max_staff and max_staff > 0 and max_staff < len(staff_rows):
        staff_rows = random.sample(list(staff_rows), max_staff)

    window_start = now - datetime.timedelta(hours=24)
    events: List[Dict[str, str]] = []
    for staff in staff_rows:
        events.extend(generate_badge_events_for_staff(staff, perimeter_doors, interior_doors, now, window_start, include_off_duty))
    return sorted(events, key=lambda row: row["timestamp"])


def write_events(path: Path, events: Sequence[Dict[str, str]]) -> None:
    fieldnames = [
        "timestamp",
        "staff_id",
        "first_name",
        "last_name",
        "role_title",
        "role_category",
        "department",
        "shift",
        "door_name",
        "category",
        "area",
        "door_type",
        "badge_required",
        "action",
        "access_result",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in events:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate realistic hospital badge events for the past 24 hours using staff and badged doors CSV files."
    )
    parser.add_argument("--staff-file", default="hospital_staff_500bed_4000staff.csv", help="Staff CSV file path.")
    parser.add_argument("--doors-file", default="hospital_badged_doors.csv", help="Badged doors CSV file path.")
    parser.add_argument("--output-file", default="hospital_badge_events_24h.csv", help="Output CSV file path.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible event generation.")
    parser.add_argument("--max-staff", type=int, default=0, help="Limit generation to this number of staff records.")
    parser.add_argument("--include-off-duty", action="store_true", help="Include occasional off-duty badge events.")
    args = parser.parse_args()

    random.seed(args.seed)
    staff_rows = load_csv(Path(args.staff_file))
    doors_rows = load_csv(Path(args.doors_file))
    events = generate_badging_history(
        staff_rows,
        doors_rows,
        now=datetime.datetime.now(),
        include_off_duty=args.include_off_duty,
        max_staff=args.max_staff if args.max_staff > 0 else None,
    )
    write_events(Path(args.output_file), events)

    print(f"Generated {len(events)} badge events for the last 24 hours into {args.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
