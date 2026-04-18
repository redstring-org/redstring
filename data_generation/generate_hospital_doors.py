#!/usr/bin/env python3
"""Generate a list of badged doors for hospital areas, including perimeter doors."""

import csv

INPUT_FILE = "hospital_areas_500bed.csv"
OUTPUT_FILE = "hospital_badged_doors.csv"

# Define perimeter doors
PERIMETER_DOORS = [
    "Main Entrance",
    "Emergency Department Entrance",
    "Ambulance Bay Entrance",
    "Service Entrance",
    "Loading Dock Entrance",
    "Helipad Access Door",
    "Visitor Entrance",
    "Staff Entrance"
]

# Define doors for different area types
AREA_DOORS = {
    "Patient Units/Wards": [
        "Main Ward Entrance",
        "Staff Entrance",
        "Visitor Entrance",
        "Nurse Station Access Door",
        "Patient Room Access Door",
        "Supply Room Door",
        "Medication Room Door"
    ],
    "Clinical Departments": [
        "Department Main Entrance",
        "Staff Only Entrance",
        "Equipment Storage Door",
        "Procedure Room Door",
        "Control Room Door"
    ],
    "Support Services": [
        "Department Entrance",
        "Storage Area Door",
        "Maintenance Access Door"
    ],
    "Administrative Areas": [
        "Office Entrance",
        "Conference Room Door",
        "Records Room Door"
    ],
    "Ancillary Services": [
        "Service Entrance",
        "Storage Door",
        "Equipment Access Door"
    ]
}

def get_doors_for_area(category, area):
    """Get the list of badged doors for a specific area."""
    base_doors = AREA_DOORS.get(category, ["Main Entrance", "Staff Entrance"])
    # Customize doors based on specific area names
    if "Intensive Care Unit" in area or "Care Unit" in area:
        return base_doors + ["Isolation Room Door", "Family Waiting Area Door"]
    elif "Ward" in area:
        return base_doors + ["Patient Bathroom Access", "Laundry Chute Door"]
    elif "Operating Rooms" in area:
        return base_doors + ["Sterile Supply Door", "Recovery Room Door", "Anesthesia Storage Door"]
    elif "Emergency Department" in area:
        return base_doors + ["Triage Door", "Trauma Bay Door", "Security Door"]
    elif "Radiology" in area or "MRI" in area or "CT" in area:
        return base_doors + ["Imaging Room Door", "Control Booth Door"]
    elif "Laboratory" in area:
        return base_doors + ["Biohazard Storage Door", "Chemical Storage Door"]
    else:
        return base_doors

def main():
    doors_list = []

    # Add perimeter doors
    for door in PERIMETER_DOORS:
        doors_list.append({
            "hospital_name": "Redstring General Hospital",
            "category": "Perimeter",
            "area": "Hospital Perimeter",
            "door_name": door,
            "door_type": "Perimeter Door",
            "badge_required": "Yes"
        })

    # Read areas from CSV and generate doors
    with open(INPUT_FILE, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row['category']
            area = row['area']
            doors = get_doors_for_area(category, area)
            
            for door in doors:
                doors_list.append({
                    "hospital_name": row['hospital_name'],
                    "category": row['category'],
                    "area": row['area'],
                    "door_name": door,
                    "door_type": "Area Door",
                    "badge_required": "Yes"
                })

    # Write to output CSV
    fieldnames = ["hospital_name", "category", "area", "door_name", "door_type", "badge_required"]
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(doors_list)

    print(f"Generated {len(doors_list)} badged doors in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()