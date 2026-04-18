# Data Contract and Seed Spec

## Purpose
This file defines the minimum canonical payloads, mappings, and reference rows needed to reproduce the gold scenario deterministically.

## Canonical event payloads

### 1. Cyber trigger payload
```json
{
  "event_id": "CY-0213-001",
  "source": "identity_risk_engine",
  "event_type": "vendor_remote_access_anomaly",
  "occurred_at": "2026-04-18T02:13:00-04:00",
  "campus_id": "RMC-MAIN",
  "account": "jmercer@vendorco",
  "person_name": "John Mercer",
  "company": "VendorCo",
  "role": "Biomedical contractor",
  "device_status": "unexpected_new_device",
  "vpn_result": "success",
  "session_active": true,
  "risk_reason": "Successful VPN login from new device while remote session remains active"
}
```

### 2. Badge/access payload
```json
{
  "event_id": "AC-0224-001",
  "source": "access_control",
  "event_type": "badge_entry",
  "occurred_at": "2026-04-18T02:24:00-04:00",
  "campus_id": "RMC-MAIN",
  "badge_id": "B-1842",
  "door_id": "SE-3",
  "door_name": "South Service Entrance SE-3",
  "access_result": "granted",
  "after_hours": true
}
```

### 3. Suspicious-person report payload
```json
{
  "event_id": "IR-0231-001",
  "source": "protective_services_officer_report",
  "event_type": "suspicious_person_report",
  "occurred_at": "2026-04-18T02:31:00-04:00",
  "campus_id": "RMC-MAIN",
  "reporter_id": "OFFICER-17",
  "reporter_role": "Protective Services Officer",
  "zone_id": "Z-IMAGING-CORRIDOR",
  "location_label": "Imaging Service Corridor",
  "description": "Male in VendorCo jacket moving two equipment cases toward Imaging Service Corridor; no escort observed."
}
```

## Reference data

### 4. Contractor identity record
```json
{
  "person_id": "P-1007",
  "full_name": "John Mercer",
  "account": "jmercer@vendorco",
  "company": "VendorCo",
  "role": "Biomedical contractor",
  "badge_id": "B-1842",
  "badge_status": "active",
  "night_schedule_status": "unknown",
  "approved_after_hours_work_order": "unknown",
  "escort_required_after_hours": true
}
```

### 5. Badgeholder mapping
```json
{
  "badge_id": "B-1842",
  "person_id": "P-1007",
  "full_name": "John Mercer",
  "company": "VendorCo",
  "mapping_type": "exact"
}
```

### 6. Door-to-zone mapping
```json
{
  "door_id": "SE-3",
  "door_name": "South Service Entrance SE-3",
  "building_id": "BLDG-SOUTH-01",
  "building_name": "South Service Wing",
  "zone_id": "Z-SOUTH-SERVICE-ENTRANCE",
  "zone_name": "South Service Entrance",
  "after_hours_sensitive": true
}
```

### 7. Zone adjacency row
```json
{
  "from_zone_id": "Z-SOUTH-SERVICE-ENTRANCE",
  "to_zone_id": "Z-IMAGING-CORRIDOR",
  "relationship": "adjacent_one_hop_same_building",
  "building_id": "BLDG-SOUTH-01"
}
```

## Optional OSINT payload example
```json
{
  "event_id": "OS-0208-001",
  "source": "public_osint_feed",
  "event_type": "contextual_osint",
  "published_at": "2026-04-18T02:08:00-04:00",
  "campus_id": "RMC-MAIN",
  "source_name": "Public post or forum item",
  "url": "https://example.invalid/osint-item",
  "summary": "Possible unusual vendor activity near hospital service entrance.",
  "location_text": "South Service Entrance area"
}
```

### OSINT rules
- optional only
- provenance-preserving
- may reinforce context only
- cannot open a case
- cannot change state by itself
- cannot justify escalation by itself

## Deterministic correlation rules
1. Resolve the cyber trigger account to a contractor identity record.
2. Resolve the badge to the same person through the badgeholder mapping.
3. Require the badge event within 30 minutes of the cyber trigger.
4. Resolve the badge door to a known zone.
5. Require the suspicious-person report within 15 minutes of the matched badge event.
6. Require the report to be in the same zone or one-hop adjacent zone in the same building.

## Expected displayed reason-code strings
- `Unexpected device login succeeded on vendor contractor account`
- `Active VPN session remains live`
- `Badge B-1842 maps to John Mercer`
- `After-hours badge use at South Service Entrance SE-3`
- `Officer report in adjacent Imaging Service Corridor within seven minutes`
- `No escort observed`
- `No linked on-campus evidence yet`
- `Contractor schedule not yet confirmed`
- `Remote session legitimacy not yet confirmed`

## Expected state progression
- after `CY-0213-001` -> **Observe**
- after `AC-0224-001` -> **Verify Now**
- after `IR-0231-001` -> **Escalate Now**

## Expected next-action outputs
- **Observe:** `Call the SOC now to confirm whether the active VPN session for jmercer@vendorco is still live and whether the MFA approval was legitimate.`
- **Verify Now:** `Call the VendorCo night supervisor now to confirm whether John Mercer is scheduled onsite and carrying badge B-1842.`
- **Escalate Now:** `Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.`

## Implementation note
These payloads and rows are sufficient for the core deterministic demo. Everything else is secondary until the gold scenario runs cleanly end to end.
