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
