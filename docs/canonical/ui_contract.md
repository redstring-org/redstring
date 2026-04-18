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
