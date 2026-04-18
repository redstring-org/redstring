## RedString

**Hackathon Project**
When everyone else sees noise, RedString sees the pattern.  

### setup venv
python3 -m venv .venv
source ./.venv/bin/activate


in a 500 bed hospital with 4000 staff

To seed, run:

1. python3 generate_hospital_staff_csv.py
2. python3 generate_hospital_areas.py
3. python3 generate_hospital_doors.py
4. python3 generate_hospital_badging_events.py --output-file hospital_badge_events_24h.csv --max-staff 500


### Example od badged data events
timestamp,staff_id,first_name,last_name,role_title,role_category,department,shift,door_name,category,area,door_type,badge_required,action,access_result
2026-04-18 07:45:00,3109,Jamie,Williams,Transport Aide,Support services,Security,Rotating,Visitor Entrance,Perimeter,Hospital Perimeter,Perimeter Door,Yes,enter,Granted
2026-04-18 07:45:00,33,Harper,Thomas,Quality Improvement Specialist,Specialized roles,Quality Improvement,Rotating,Emergency Department Entrance,Perimeter,Hospital Perimeter,Perimeter Door,Yes,enter,Granted
2026-04-18 07:46:00,2167,Eli,Smith,Licensed Practical Nurse,Clinical staff,Surgical,Rotating,Loading Dock Entrance,Perimeter,Hospital Perimeter,Perimeter Door,Yes,enter,Granted
2026-04-18 07:47:00,3968,Quinn,Brown,Clinical Nurse Specialist,Clinical staff,Nursing,Rotating,Main Entrance,Perimeter,Hospital Perimeter,Perimeter Door,Yes,enter,Granted
