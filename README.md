## RedString

**Hackathon Project**
When everyone else sees noise, RedString sees the pattern.  

### setup venv
python3 -m venv .venv
source ./.venv/bin/activate


in a 500 bed hospital with 4000 staff

To seed, run:

1.
```bash
python3 generate_hospital_staff_csv.py
```
2.
```bash
python3 generate_hospital_areas.py
```
3. 
```bash
python3 generate_hospital_doors.py
```
4. 
```bash
python3 generate_hospital_badging_events.py --output-file hospital_badge_events_24h.csv --max-staff 500
```


### Example of badged data events
```bash
timestamp,staff_id,first_name,last_name,role_title,role_category,department,shift,door_name,category,area,door_type,badge_required,action,access_result
2026-04-18T07:45:00.000+00:00Z,11,Taylor,Davis,Registered Nurse,Clinical staff,Laboratory,Rotating,Main Entrance,Perimeter,Hospital Perimeter,Perimeter Door,Yes,enter,Granted
2026-04-18T07:45:00.000+00:00Z,150,Bailey,Williams,Anesthesiologist,Specialized roles,Infection Control,Rotating,Visitor Entrance,Perimeter,Hospital Perimeter,Perimeter Door,Yes,enter,Granted
2026-04-18T07:45:00.000+00:00Z,335,Neil,Perez,Radiologic Technologist,Clinical staff,Surgical,Rotating,Emergency Department Entrance,Perimeter,Hospital Perimeter,Perimeter Door,Yes,enter,Granted
2026-04-18T07:45:00.000+00:00Z,469,Skyler,Williams,Pharmacist,Specialized roles,Anesthesia,Rotating,Loading Dock Entrance,Perimeter,Hospital Perimeter,Perimeter Door,Yes,enter,Granted
2026-04-18T07:45:00.000+00:00Z,991,Sydney,Moore,Patient Care Assistant,Support services,Facilities,Rotating,Service Entrance,Perimeter,Hospital Perimeter,Perimeter Door,Yes,enter,Granted
2026-04-18T07:45:00.000+00:00Z,1051,Mia,Martinez,Registered Nurse,Clinical staff,Surgical,Rotating,Service Entrance,Perimeter,Hospital Perimeter,Perimeter Door,Yes,enter,Granted
```

### Scrape the latest 20 X posts
Install Playwright once in the active virtualenv:

```bash
pip install playwright
playwright install chromium
```

Run the scraper:

```bash
python3 scrape_x_posts_to_csv.py --account-url https://x.com/DCPoliceDept --limit 20 --output-file dcpolicedept_last_20_posts.csv
```

If X blocks headless browsing, retry with a visible browser window:

```bash
python3 scrape_x_posts_to_csv.py --account-url https://x.com/DCPoliceDept --limit 20 --output-file dcpolicedept_last_20_posts.csv --headful
```

### Example of Twitter data from DC Police
```bash
post_id,screen_name,posted_at,url,text,is_reply
2045539490546995340,DCPoliceDept,2026-04-18T16:26:33.000Z,https://x.com/DCPoliceDept/status/2045539490546995340,Expect road closures for several hours for the Major Crash Investigation.,no
2045535861689778540,DCPoliceDept,2026-04-18T16:12:08.000Z,https://x.com/DCPoliceDept/status/2045535861689778540,"Incident: Hit and Run crash investigation at 23rd and L Street, NW. One adult female pedestrian critically injured. Driver fled the scene. Lookout for a white Jeep with MD tags.",no
2045503770121978233,DCPoliceDept,2026-04-18T14:04:37.000Z,https://x.com/DCPoliceDept/status/2045503770121978233,Taylor Simmons has been located. Thank you for your help.,no
```

### POST badge events to a local ingest API
Read the generated badge events CSV and send each row as JSON to the ingest endpoint:

```bash
python3 post_badge_events_csv.py --csv-file hospital_badge_events_24h.csv --endpoint http://localhost/api/ingest
```

Stop on the first failed request:

```bash
python3 post_badge_events_csv.py --csv-file hospital_badge_events_24h.csv --endpoint http://localhost/api/ingest --stop-on-error
```
