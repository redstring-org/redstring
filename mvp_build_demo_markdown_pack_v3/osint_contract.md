# OSINT Contract

## Purpose
Define the exact role, limits, and handling rules for optional OSINT in the MVP.

## Status
OSINT is optional contextual input only.

It is:
- configurable by deployment
- provenance-preserving
- collapsed by default in the UI
- not required in the gold demo
- not allowed to drive escalation by itself

## What OSINT may do
OSINT may:
- attach contextual evidence to an already-open case
- reinforce time and place context for the same facility
- provide an additional breadcrumb for operator awareness
- preserve a pointer back to the originating public source

## What OSINT may not do
OSINT may not:
- open a case by itself
- move a case to **Verify Now** by itself
- move a case to **Escalate Now** by itself
- replace the suspicious-person report in the gold scenario
- outrank the cyber trigger, badge event, or suspicious-person report in the UI
- appear as a primary panel on the first screen
- appear without provenance

## Minimum provenance fields
Every OSINT item must preserve:
- source label
- source type
- timestamp observed
- URL or retrievable source pointer
- facility or location hint
- ingestion timestamp

## Minimum matching rules
An OSINT item may attach to the case only if all of the following are true:
1. it matches the same hospital facility or immediate vicinity
2. it falls within the relevant time window for the open case
3. it has preserved provenance
4. it does not contradict the locked deterministic core logic

## UI rules
If OSINT is enabled:
- it must be collapsed by default
- it must appear below the three core evidence items
- it must be clearly labeled as contextual
- it must never displace the state, next action, timeline, why linked, or what weakens it

## Gold demo rule
The core demo must succeed with OSINT fully disabled.

If OSINT is shown in a secondary branch, it may only be used to say:
- `Additional public context exists for the same facility and time window.`

It may not be used to say:
- `This is why the case escalated.`
- `This replaces the officer report.`
- `This proves intent.`

## Suggested OSINT event shape
```json
{
  "osint_event_id": "OS-0228-001",
  "source_label": "public forum post",
  "source_type": "forum",
  "observed_at": "2026-04-18T02:28:00-04:00",
  "ingested_at": "2026-04-18T02:29:10-04:00",
  "facility_hint": "hospital south service entrance",
  "location_hint": "service entrance / loading corridor",
  "url": "https://example.invalid/post/123",
  "summary": "Report of unusual vendor equipment movement near hospital service entrance.",
  "provenance_status": "preserved",
  "allowed_role": "context_only"
}
```

## Acceptance checks
Optional OSINT is compliant only if:
- disabling it does not change core behavior
- enabling it does not change state progression
- enabling it does not change the selected next action
- enabling it does not change escalation eligibility
- provenance is visible to the operator
