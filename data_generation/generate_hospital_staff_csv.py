#!/usr/bin/env python3
"""Generate a hospital staff CSV for a 500-bed hospital with 4000 staff."""

import csv
import random
from datetime import datetime

OUTPUT_FILE = "hospital_staff_500bed_4000staff.csv"
HOSPITAL_NAME = "Redstring General Hospital"
HOSPITAL_BEDS = 500
STAFF_COUNT = 4000

ROLE_CATEGORIES = [
    "Clinical staff",
    "Support services",
    "Administrative staff",
    "Specialized roles",
]

DEPARTMENTS = {
    "Clinical staff": [
        "Nursing",
        "Medical",
        "Surgical",
        "Emergency",
        "Radiology",
        "Laboratory",
    ],
    "Support services": [
        "Housekeeping",
        "Facilities",
        "Food services",
        "Transport",
        "Security",
        "Patient support",
    ],
    "Administrative staff": [
        "Finance",
        "Human Resources",
        "Medical Records",
        "Admissions",
        "Billing",
        "IT",
    ],
    "Specialized roles": [
        "Pharmacy",
        "Anesthesia",
        "Rehabilitation",
        "Infection Control",
        "Quality Improvement",
        "Clinical Research",
    ],
}

FIRST_NAMES = [
    "Avery", "Jordan", "Morgan", "Taylor", "Casey", "Riley", "Jamie", "Skyler",
    "Alex", "Dakota", "Cameron", "Peyton", "Rowan", "Quinn", "Jordan",
    "Harper", "Sydney", "Bailey", "Reese", "Neil", "Noah", "Eli", "Mia", "Chloe",
    "Liam", "Emma", "Olivia", "Sophia", "Jackson", "Aiden", "Lucas", "Mason",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
]

SHIFTS = ["Day", "Evening", "Night", "Rotating"]
DAYS_OF_WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

ROLE_TITLES = {
    "Clinical staff": [
        "Registered Nurse",
        "Licensed Practical Nurse",
        "Physician",
        "Physician Assistant",
        "Medical Technologist",
        "Radiologic Technologist",
        "Clinical Nurse Specialist",
    ],
    "Support services": [
        "Housekeeper",
        "Maintenance Technician",
        "Food Service Worker",
        "Transport Aide",
        "Security Officer",
        "Patient Care Assistant",
    ],
    "Administrative staff": [
        "Office Administrator",
        "Billing Specialist",
        "HR Coordinator",
        "Medical Records Clerk",
        "IT Support Specialist",
        "Finance Analyst",
    ],
    "Specialized roles": [
        "Pharmacist",
        "Anesthesiologist",
        "Physical Therapist",
        "Infection Control Nurse",
        "Quality Improvement Specialist",
        "Clinical Research Coordinator",
    ],
}


def random_phone_number():
    return f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"


def random_schedule_days(role_category, shift):
    if shift == "Rotating":
        pattern = random.choice([
            ["Mon", "Tue", "Wed", "Thu", "Fri"],
            ["Wed", "Thu", "Fri", "Sat", "Sun"],
            ["Thu", "Fri", "Sat", "Sun"],
            ["Mon", "Tue", "Wed", "Thu"],
        ])
        if role_category == "Clinical staff":
            pattern = random.choice([
                ["Mon", "Tue", "Wed", "Thu", "Fri"],
                ["Thu", "Fri", "Sat", "Sun"],
                ["Sat", "Sun", "Mon", "Tue"],
                ["Wed", "Thu", "Fri", "Sat", "Sun"],
            ])
        return pattern

    days = DAYS_OF_WEEK.copy()
    if role_category == "Administrative staff":
        days = days[:5]

    if shift == "Day":
        available = days[:5]
        k = 5 if len(available) >= 5 else len(available)
        chosen = random.sample(available, k=k)
    elif shift == "Evening":
        choices = days[:6] if random.random() < 0.5 else days
        k = 5 if len(choices) >= 5 else len(choices)
        chosen = random.sample(choices, k=k)
    else:
        weekend_bias = ["Sat", "Sun"] if random.random() < 0.4 else days
        if len(weekend_bias) <= 2:
            k = random.choice([1, 2])
        else:
            k = random.choice([3, 4])
        chosen = random.sample(weekend_bias, k=k)
    chosen.sort(key=lambda x: DAYS_OF_WEEK.index(x))
    return chosen


def shift_time_range(shift):
    if shift == "Day":
        return random.choice(["07:00", "08:00"]), random.choice(["15:00", "16:00"])
    if shift == "Evening":
        return "15:00", "23:00"
    if shift == "Night":
        return random.choice(["23:00", "22:00"]), random.choice(["06:00", "07:00"])
    return "Varies", "Varies"


def is_on_duty_today(schedule_days):
    today = DAYS_OF_WEEK[datetime.today().weekday()]
    return "Yes" if today in schedule_days else "No"


def random_years_experience():
    return random.randint(1, 35)


def random_email(first_name, last_name, staff_id):
    local = f"{first_name.lower()}.{last_name.lower()}"
    return f"{local}.{staff_id}@redstringhospital.org"


def build_staff_records(count):
    records = []
    for staff_id in range(1, count + 1):
        role_category = random.choices(
            ROLE_CATEGORIES,
            weights=[0.45, 0.20, 0.20, 0.15],
            k=1,
        )[0]
        department = random.choice(DEPARTMENTS[role_category])
        role = random.choice(ROLE_TITLES[role_category])
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        years_experience = random_years_experience()
        shift = random.choices(
            SHIFTS,
            weights=(
                [0.35, 0.25, 0.25, 0.15]
                if role_category == "Clinical staff"
                else [0.45, 0.20, 0.10, 0.25]
                if role_category == "Support services"
                else [0.65, 0.15, 0.05, 0.15]
                if role_category == "Administrative staff"
                else [0.45, 0.20, 0.10, 0.25]
            ),
            k=1,
        )[0]
        schedule_days = random_schedule_days(role_category, shift)
        shift_start, shift_end = shift_time_range(shift)
        records.append({
            "staff_id": staff_id,
            "hospital_name": HOSPITAL_NAME,
            "hospital_beds": HOSPITAL_BEDS,
            "first_name": first_name,
            "last_name": last_name,
            "role_category": role_category,
            "role_title": role,
            "department": department,
            "shift": shift,
            "shift_start": shift_start,
            "shift_end": shift_end,
            "schedule_days": ",".join(schedule_days),
            "on_duty_today": is_on_duty_today(schedule_days),
            "years_experience": years_experience,
            "email": random_email(first_name, last_name, staff_id),
            "phone": random_phone_number(),
        })
    return records


def write_csv(records, output_file):
    fieldnames = [
        "staff_id",
        "hospital_name",
        "hospital_beds",
        "first_name",
        "last_name",
        "role_category",
        "role_title",
        "department",
        "shift",
        "shift_start",
        "shift_end",
        "schedule_days",
        "on_duty_today",
        "years_experience",
        "email",
        "phone",
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main():
    staff = build_staff_records(STAFF_COUNT)
    write_csv(staff, OUTPUT_FILE)
    print(
        f"Generated {len(staff)} staff records for a "
        f"{HOSPITAL_BEDS}-bed hospital into '{OUTPUT_FILE}'."
    )


if __name__ == "__main__":
    main()
