#!/usr/bin/env python3
"""Generate a large hospital badge events CSV for streaming demos."""
from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

STAFF = [
    (1,  "Emma",    "Thompson",  "Registered Nurse",        "Clinical staff",      "Emergency",       "Day"),
    (2,  "James",   "Rodriguez", "Physician",               "Medical staff",       "Cardiology",      "Night"),
    (3,  "Sarah",   "Kim",       "Pharmacist",              "Specialized roles",   "Pharmacy",        "Rotating"),
    (4,  "Michael", "Chen",      "Security Officer",        "Security",            "Protective Svcs", "Night"),
    (5,  "Laura",   "Patel",     "Lab Technician",          "Clinical staff",      "Laboratory",      "Day"),
    (6,  "David",   "Okafor",    "Radiologic Technologist", "Clinical staff",      "Radiology",       "Rotating"),
    (7,  "Priya",   "Singh",     "Anesthesiologist",        "Medical staff",       "Surgical",        "Day"),
    (8,  "Carlos",  "Mendez",    "Physical Therapist",      "Specialized roles",   "Rehabilitation",  "Day"),
    (9,  "Aisha",   "Williams",  "Patient Care Tech",       "Clinical staff",      "ICU",             "Night"),
    (10, "Tom",     "Nakamura",  "IT Support Specialist",   "Support staff",       "IT",              "Day"),
    (11, "Grace",   "Osei",      "Social Worker",           "Support staff",       "Psychiatry",      "Day"),
    (12, "Ben",     "Harris",    "Surgeon",                 "Medical staff",       "Surgical",        "Day"),
    (13, "Nina",    "Johansson", "Nurse Practitioner",      "Clinical staff",      "Oncology",        "Rotating"),
    (14, "Felix",   "Brown",     "Housekeeping Staff",      "Facilities",          "Facilities",      "Night"),
    (15, "Mia",     "Davis",     "Dietitian",               "Specialized roles",   "Nutrition",       "Day"),
    (16, "Omar",    "Hassan",    "Security Officer",        "Security",            "Protective Svcs", "Night"),
    (17, "Yuki",    "Tanaka",    "Radiologist",             "Medical staff",       "Radiology",       "Day"),
    (18, "Chloe",   "Martin",    "Respiratory Therapist",   "Clinical staff",      "Pulmonology",     "Rotating"),
    (19, "Aaron",   "Lewis",     "Maintenance Tech",        "Facilities",          "Facilities",      "Night"),
    (20, "Sofia",   "Garcia",    "Pediatric Nurse",         "Clinical staff",      "Pediatrics",      "Day"),
]

DOORS = [
    ("Main Entrance",              "Perimeter",  "Hospital Perimeter",    "Perimeter Door"),
    ("Emergency Department Entrance", "Perimeter", "Hospital Perimeter",  "Perimeter Door"),
    ("Staff Parking Entrance",     "Perimeter",  "Hospital Perimeter",    "Perimeter Door"),
    ("Loading Dock Entrance",      "Perimeter",  "Hospital Perimeter",    "Perimeter Door"),
    ("South Service Entrance SE-3","Internal",   "Service Corridor",      "Interior Door"),
    ("ICU Corridor Door",          "Internal",   "ICU",                   "Interior Door"),
    ("Pharmacy Secure Door",       "Restricted", "Pharmacy",              "Secure Door"),
    ("Surgical Suite Entry",       "Restricted", "Surgical Suite",        "Secure Door"),
    ("Imaging Service Corridor",   "Internal",   "Radiology",             "Interior Door"),
    ("Server Room",                "Restricted", "IT Infrastructure",     "Secure Door"),
    ("Morgue Corridor",            "Internal",   "Pathology",             "Interior Door"),
    ("Rooftop Access",             "Restricted", "Building Services",     "Secure Door"),
    ("Visitor Entrance",           "Perimeter",  "Hospital Perimeter",    "Perimeter Door"),
    ("Chapel Corridor",            "Internal",   "Common Areas",          "Interior Door"),
    ("Lab Access Door",            "Restricted", "Laboratory",            "Secure Door"),
]


def generate(count: int = 500, start: datetime | None = None) -> list[dict]:
    if start is None:
        start = datetime(2026, 4, 18, 6, 0, 0, tzinfo=timezone.utc)

    rows = []
    t = start
    for _ in range(count):
        t += timedelta(seconds=random.randint(10, 120))
        staff = random.choice(STAFF)
        door = random.choice(DOORS)
        result = "Granted" if random.random() < 0.93 else "Denied"
        rows.append({
            "timestamp":    t.isoformat(),
            "staff_id":     staff[0],
            "first_name":   staff[1],
            "last_name":    staff[2],
            "role_title":   staff[3],
            "role_category": staff[4],
            "department":   staff[5],
            "shift":        staff[6],
            "door_name":    door[0],
            "category":     door[1],
            "area":         door[2],
            "door_type":    door[3],
            "badge_required": "Yes",
            "action":       "enter",
            "access_result": result,
        })
    return rows


def main() -> None:
    rows = generate(500)
    out = SCRIPT_DIR / "hospital_badge_events_24h.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
