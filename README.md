# RedString
**When everyone else sees noise, RedString sees patterns**

Deterministic MVP for the Cyber-Physical Correlation Engine.


## Start Here

Read these files first and treat them as binding:

1. `docs/canonical/prd_v1_2_osint_update.md`
2. `docs/canonical/gold_scenario.md`
3. `docs/canonical/acceptance_criteria.md`
4. `docs/canonical/ui_contract.md`
5. `docs/canonical/data_contract_and_seed_spec.md`
6. `docs/build/build_project_instructions.md`
7. `docs/build/event_injection_runbook.md`
8. `docs/build/demo_contract.md`

## Current MVP Shape

- one hospital campus
- one operator: Hospital Security Duty Manager
- one qualifying cyber trigger only
- one matched badge/access event
- one suspicious-person report
- one active case only
- one active case card
- deterministic `Observe -> Verify Now -> Escalate Now`
- deterministic next-action matrix
- AI-off fallback via deterministic template text
- no chatbot
- no queue-first UI
- no map-first UI

## Repo Layout

- `docs/canonical/` locked product and implementation contracts
- `docs/build/` demo build and runbook docs
- `docs/reference/` optional rationale notes
- `fixtures/` deterministic gold-scenario data
- `engine/` deterministic correlation logic and state services
- `app/` active case-card rendering runtime
- `scripts/` inject/reset/demo commands
- `tests/` unit and integration acceptance paths
- `src/` shared seed constants, schemas, and fixture loaders reused by the engine

## Commands

- `npm run build`
- `npm run demo:reset`
- `npm run demo:inject:cyber`
- `npm run demo:inject:badge`
- `npm run demo:inject:report`
- `npm run demo:render`
- `npm test`

## Definition Of Done

The MVP is only done when the locked three-event flow runs end to end and the acceptance criteria pass exactly.

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

### Example of Twitter data from DC Police
```bash
post_id,screen_name,posted_at,url,text,is_reply
2045539490546995340,DCPoliceDept,2026-04-18T16:26:33.000Z,https://x.com/DCPoliceDept/status/2045539490546995340,Expect road closures for several hours for the Major Crash Investigation.,no
2045535861689778540,DCPoliceDept,2026-04-18T16:12:08.000Z,https://x.com/DCPoliceDept/status/2045535861689778540,"Incident: Hit and Run crash investigation at 23rd and L Street, NW. One adult female pedestrian critically injured. Driver fled the scene. Lookout for a white Jeep with MD tags.",no
2045503770121978233,DCPoliceDept,2026-04-18T14:04:37.000Z,https://x.com/DCPoliceDept/status/2045503770121978233,Taylor Simmons has been located. Thank you for your help.,no
```

### Example of Suspicious person event
```bash
report_id,occurred_at,reporter,location,description,verified,person_removed
SPR-0001,2026-04-18T06:05:54.156Z,medical staff,Emergency Department Ambulance Bay,Person in mismatched scrubs observed pushing unattended equipment cases toward Emergency Department Ambulance Bay.,yes,yes
SPR-0002,2026-04-18T06:46:54.156Z,security,Emergency Department Ambulance Bay,Visitor was reported watching shift change activity near Emergency Department Ambulance Bay and recording on a phone.,yes,no
SPR-0003,2026-04-18T07:22:54.156Z,patient,Imaging Service Corridor,Visitor was reported watching shift change activity near Imaging Service Corridor and recording on a phone.,yes,yes
SPR-0004,2026-04-18T07:52:54.156Z,visitor,Pharmacy Hallway,Unidentified person photographed badge readers and access panels near Pharmacy Hallway.,no,no
SPR-0005,2026-04-18T08:29:54.156Z,medical staff,Labor and Delivery Waiting Area,Unknown person was seen moving a supply cart through Labor and Delivery Waiting Area and could not explain where it came from.,no,no
```
