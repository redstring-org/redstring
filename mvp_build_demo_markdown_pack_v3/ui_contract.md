# UI Contract

## Primary rule
The first screen must be the active case card for the gold scenario.

## What the first screen must show
- **case title**
- **location**
- **state**
- **primary subject**
- **trigger summary**
- **timeline**
- **why linked**
- **what weakens it**
- **next human check**
- **escalation recommendation**
- **provenance**

## Locked gold-scenario values
- **case title:** `VendorCo contractor remote-access anomaly with potential on-campus linkage`
- **location:** `South Service Entrance SE-3 / Imaging Service Corridor`
- **primary subject:** `John Mercer (VendorCo biomedical contractor)`
- **trigger summary:** `Successful VPN login from a new device while the remote session remains active.`
- **escalation recommendation when state = Escalate Now:** `Notify protective services leadership and SOC now.`

## Visual hierarchy
1. state badge
2. next human check
3. timeline
4. why linked
5. what weakens it
6. escalation recommendation when state is **Escalate Now**
7. provenance chips or labels

## What must be visible
- state badge: **Observe**, **Verify Now**, or **Escalate Now**
- primary subject
- trigger summary
- the three-event timeline with timestamps
- why linked text using the deterministic reason-code strings
- what weakens it text
- one next human check
- escalation recommendation when the state reaches **Escalate Now**
- provenance labels for each evidence item, including source and timestamp

## What can be hidden
- numeric score
- raw event JSON
- internal IDs
- debug factor breakdown
- backend latency details
- OSINT drawer or stub
- any small static map used only for internal debugging

## What must not appear on the first demo screen
- empty case queue
- freeform chat box
- campus map as a primary panel
- multiple trigger-type selectors
- unresolved-items section as a separate module
- raw SOC console views
- raw access-control console views
- OSINT panel as a primary module
- prominent numeric score

## OSINT display rule
If OSINT is enabled, it must be collapsed by default, shown only as contextual support, and visually subordinate to the cyber trigger, badge event, and suspicious-person report.

## Anti-drift rule
If a UI element competes with the active case card for attention, it probably does not belong in the MVP.
