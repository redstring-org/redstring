#!/usr/bin/env python3
"""Enumerate different areas in a 500-bed hospital."""

import csv

OUTPUT_FILE = "hospital_areas_500bed.csv"
HOSPITAL_NAME = "Redstring General Hospital"
HOSPITAL_BEDS = 500

HOSPITAL_AREAS = {
    "Patient Units/Wards": [
        "General Medicine Ward (Multiple floors)",
        "Surgical Ward",
        "Intensive Care Unit (ICU)",
        "Cardiac Care Unit (CCU)",
        "Neonatal Intensive Care Unit (NICU)",
        "Pediatric Intensive Care Unit (PICU)",
        "Medical Intensive Care Unit (MICU)",
        "Surgical Intensive Care Unit (SICU)",
        "Maternity Ward",
        "Postpartum Unit",
        "Pediatric Ward",
        "Oncology Ward",
        "Neurology Ward",
        "Cardiology Ward",
        "Orthopedic Ward",
        "Emergency Department Patient Bays",
        "Observation Unit",
        "Step-Down Units",
        "Rehabilitation Ward",
        "Psychiatric Ward",
        "Geriatric Ward",
        "Infectious Disease Isolation Ward",
    ],
    "Clinical Departments": [
        "Operating Rooms (OR)",
        "Emergency Department (ED)",
        "Radiology Department",
        "Laboratory",
        "Pharmacy",
        "Blood Bank",
        "Pathology",
        "Anesthesia Department",
        "Dialysis Unit",
        "Endoscopy Suite",
        "Cardiac Catheterization Lab",
        "Angiography Suite",
        "MRI Suite",
        "CT Scan Suite",
        "Ultrasound Rooms",
        "X-Ray Rooms",
        "Mammography Suite",
        "Nuclear Medicine",
        "Radiation Therapy",
        "Chemotherapy Suite",
        "Physical Therapy Department",
        "Occupational Therapy",
        "Speech Therapy",
        "Respiratory Therapy",
        "Wound Care Clinic",
        "Pain Management Clinic",
        "Sleep Study Center",
    ],
    "Support Services": [
        "Housekeeping Department",
        "Facilities/Maintenance",
        "Food Services/Kitchen",
        "Laundry Services",
        "Medical Waste Disposal",
        "Biohazard Storage",
        "Equipment Sterilization",
        "Supply Chain/Inventory",
        "Patient Transport",
        "Environmental Services",
        "Pest Control Storage",
        "HVAC Control Room",
    ],
    "Administrative Areas": [
        "Human Resources",
        "Finance Department",
        "Medical Records",
        "Admissions/Registration",
        "Billing Department",
        "IT Department",
        "Quality Assurance",
        "Risk Management",
        "Compliance Office",
        "Medical Staff Office",
        "Administration Offices",
        "Board Room",
        "Conference Rooms",
        "Training Center",
        "Library/Medical Library",
        "Research Department",
    ],
    "High-Security Areas": [
        "Operating Rooms (Restricted Access)",
        "NICU/PICU Secure Zones",
        "Emergency Department Back-of-House",
        "Psychiatric Ward Secure Units",
        "Infant Protection Zones",
        "Medication Storage Vaults",
        "Controlled Substances Room",
        "Research Labs with Biohazards",
        "Secure Patient Holding",
        "Forensic/Medical Examiner Area",
        "High-Risk Isolation Rooms",
        "Security Command Center",
    ],
    "Common Areas": [
        "Main Lobby",
        "Waiting Areas",
        "Cafeteria",
        "Gift Shop",
        "Chapel",
        "Visitor Lounges",
        "Patient Dining Areas",
        "Family Waiting Rooms",
        "Courtyard/Garden",
        "Helipad",
    ],
    "Restricted Corridors and Access Points": [
        "Staff-Only Department Entries",
        "Medication Rooms",
        "Supply Rooms",
        "IT Server Rooms",
        "Records Storage",
        "Elevators (Service/Staff)",
        "Parking (Staff/Physician)",
        "Loading Docks",
        "Restricted Corridors",
        "Service Entrances",
        "Utility Tunnels",
        "Roof Access",
        "Basement Storage",
        "Emergency Exits (Staff Only)",
    ],
}


def build_area_records():
    records = []
    for category, areas in HOSPITAL_AREAS.items():
        for area in areas:
            records.append({
                "hospital_name": HOSPITAL_NAME,
                "hospital_beds": HOSPITAL_BEDS,
                "category": category,
                "area": area,
            })
    return records


def write_csv(records, output_file):
    fieldnames = [
        "hospital_name",
        "hospital_beds",
        "category",
        "area",
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main():
    areas = build_area_records()
    write_csv(areas, OUTPUT_FILE)
    
    print("Hospital Areas in a 500-Bed Hospital")
    print("=" * 40)
    
    total_areas = 0
    for category, area_list in HOSPITAL_AREAS.items():
        print(f"\n{category}:")
        print("-" * len(category))
        for area in area_list:
            print(f"  - {area}")
        total_areas += len(area_list)
    
    print(f"\nTotal enumerated areas: {total_areas}")
    print(f"Generated {len(areas)} area records into '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()