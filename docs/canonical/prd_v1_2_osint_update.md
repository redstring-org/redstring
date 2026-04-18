# Cyber-Physical Correlation Engine
## PRD v1.2 MVP / Build-Handoff / OSINT Update

**Date:** April 18, 2026  
**Product type:** Deterministic cross-domain case engine  
**Status:** Canonical source of truth for MVP Build + Demo

## 1. Final recommendation

Cyber-Physical Correlation Engine is a **deterministic cross-domain case engine** for **one hospital campus** and **one operator: the Hospital Security Duty Manager**. A case is opened upstream by **SOC or identity tooling** from **one qualifying trigger only**: a successful VPN login from an unexpected device on a biomedical contractor account while the remote session remains active. The product then deterministically links that trigger to **one badge/access event** and **one suspicious-person report**, promotes the case through **Observe -> Verify Now -> Escalate Now**, and renders **one active case card** with grounded evidence, deterministic reason codes, one deterministic next human check, and one concrete escalation recommendation: **Notify protective services leadership and SOC now.** AI is used only to phrase grounded facts, deterministic reason codes, contradictions, missing evidence, and the selected next human check.

This version preserves the locked MVP shape and adds the final OSINT rule: **OSINT is optional contextual input only**. It is configurable by deployment, provenance-preserving, collapsed by default in the UI, not required in the gold demo, and not allowed to drive escalation by itself.

## 2. Product overview

Cyber-Physical Correlation Engine helps an **on-shift Hospital Security Duty Manager** decide when a suspicious vendor remote-access event has become a real campus incident. The duty manager does not work inside cyber consoles. Instead, **SOC or identity tooling opens the case first**, and the duty manager receives one assembled case card that combines the cyber trigger with campus evidence and tells them whether to **Observe**, **Verify Now**, or **Escalate Now**.

This MVP is intentionally narrow:
- one hospital campus
- one duty manager
- one qualifying cyber trigger
- one badge/access feed
- one suspicious-person report feed
- one optional OSINT input that is contextual only
- one active case card
- one deterministic next human check
- one deterministic escalation target

## 3. Operator framing

### Primary operator
**Hospital Security Duty Manager**

### Upstream handoff
The duty manager receives a case that was already opened by **SOC or identity tooling**. The duty manager is not expected to inspect raw VPN telemetry, identity graphs, or SOC consoles directly in the MVP.

### Exact decision
**Has this vendor remote-access anomaly crossed the threshold from a cyber exception into a campus incident that requires immediate operational follow-up and notification of protective services leadership and SOC?**

## 4. Goal and non-goals

### Goal
Help the Hospital Security Duty Manager make a faster, more defensible escalation decision from one already-opened cyber case.

### Non-goals
- No chatbot workflow
- No broad SOC search surface
- No multi-campus command view
- No autonomous response
- No generalized threat detection platform
- No multiple trigger classes in the MVP
- No OSINT in the main demo path or first-screen UI
- No model-driven correlation or model-driven confidence scoring
- No queue-first or map-first primary experience

## 5. Locked MVP scope

### Single qualifying trigger
Use only this trigger:

`Vendor remote-access anomaly on a biomedical contractor account: successful VPN login from an unexpected device while the remote session remains active.`

### In-scope feeds
Use only:
- cyber trigger
- badge/access event
- suspicious-person report
- contractor identity record
- badgeholder mapping
- door-to-zone mapping
- zone adjacency row
- optional OSINT event for contextual reinforcement only

### Explicitly out of scope for the demo
- OSINT as a required signal
- OSINT as a primary panel on the first screen
- OSINT opening a case
- OSINT changing state by itself
- OSINT justifying escalation by itself
- multiple cyber trigger types
- empty queue opening state
- campus map as a primary UI surface
- unresolved-items panel as a separate product surface
- AI ranking of evidence
- AI selection of next action
- AI determination of correlation
- AI determination of confidence state

## 6. Locked gold incident

Use this exact incident path in the demo:

- `02:13 AM — jmercer@vendorco successful VPN login from a new device`
- `02:24 AM — badge B-1842 used at South Service Entrance SE-3 after hours`
- `02:31 AM — officer report: male in VendorCo jacket moving two equipment cases toward Imaging Service Corridor; no escort observed`

### Required state transitions
- Event 1 -> **Observe**
- Event 2 -> **Verify Now**
- Event 3 -> **Escalate Now**

## 7. Deterministic case logic

### 7.1 Correlation rules
The MVP must use deterministic logic only.

A case is linked when these conditions are met:
1. The cyber trigger resolves to a known contractor identity record.
2. A badge/access event maps to the same contractor through the badgeholder mapping.
3. The badge/access event occurs within **30 minutes** of the cyber trigger.
4. The badge/access event occurs at a mapped door with a known zone.
5. A suspicious-person report occurs within **15 minutes** of the matched badge/access event.
6. The suspicious-person report lands in the **same zone or a one-hop adjacent zone in the same building**.

### 7.2 State rules
- **Observe**
  - Opened by the qualifying cyber trigger alone.
  - No on-campus corroboration is yet linked.
  - Escalation is not allowed.

- **Verify Now**
  - Requires the qualifying cyber trigger plus one linked badge/access event for the same mapped subject within the time window.
  - Escalation is still not allowed in the MVP.
  - The operator must perform a human verification check first.

- **Escalate Now**
  - Requires the qualifying cyber trigger, the linked badge/access event, and the linked suspicious-person report in the same or adjacent zone within the time window.
  - Escalation is allowed.
  - The case card must show the escalation recommendation: **Notify protective services leadership and SOC now.**

### 7.3 Optional OSINT rule
Optional OSINT may be attached to the case only when it matches the same facility and relevant time window and preserves source provenance. It may add context, but it cannot open the case, cannot move a case to **Verify Now** or **Escalate Now** by itself, and cannot replace the suspicious-person report in the MVP.

### 7.4 Numeric score policy
A numeric score may exist only as a hidden or debug-facing implementation detail. It must not be primary in the UI. The visible primary output is always the decision state:
- **Observe**
- **Verify Now**
- **Escalate Now**

## 8. Deterministic next-action contract

Use this exact next-action matrix:

- unresolved identity -> `Call the VendorCo night supervisor now to confirm whether John Mercer is scheduled onsite and carrying badge B-1842.`
- unresolved physical presence -> `Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.`
- unresolved remote session legitimacy -> `Call the SOC now to confirm whether the active VPN session for jmercer@vendorco is still live and whether the MFA approval was legitimate.`

### Selection rule
Select the next human check deterministically in this order:
1. If the case is **Escalate Now** and physical presence is unresolved, select **dispatch officer**.
2. Else if a badge event is linked and identity or schedule is unresolved, select **call VendorCo night supervisor**.
3. Else select **call SOC** to validate the active remote session.

AI may only phrase the selected action clearly. AI does not choose it.

## 9. AI boundary

AI may only:
- explain grounded case facts
- phrase deterministic reason codes in operator language
- phrase contradictions and missing evidence without adding new facts
- phrase the selected next human check clearly

AI must not:
- rank core evidence in the MVP
- select the next action
- determine correlation
- determine confidence state
- invent facts, identities, or explanations not present in the case JSON

### Failure mode requirement
If AI phrasing fails or is unavailable, the product must still function by rendering deterministic template text from the same case JSON.

## 10. Functional requirements

The MVP must:
1. Accept only the single locked cyber trigger type.
2. Open a case from SOC or identity tooling, not from the duty manager manually.
3. Resolve `jmercer@vendorco` to the contractor identity record for John Mercer.
4. Resolve badge `B-1842` to the same subject through the badgeholder mapping.
5. Map door `SE-3` to `South Service Entrance SE-3` and its adjacent zone relation to `Imaging Service Corridor`.
6. Promote the case from **Observe** to **Verify Now** only after the linked badge/access event arrives.
7. Promote the case from **Verify Now** to **Escalate Now** only after the linked suspicious-person report arrives.
8. Select the next human check from the deterministic next-action matrix.
9. Render one active case card without requiring a queue-first experience.
10. Show why linked, what weakens it, and provenance for every visible event.
11. Show the escalation recommendation only when the case reaches **Escalate Now**.
12. Support the full core demo with OSINT disabled.
13. If OSINT is enabled, keep it collapsed by default and provenance-preserving.
14. Support the full demo without a campus map.
15. Support the full demo without any freeform chat interface.

## 11. Acceptance-test strings

### Exact displayed reason-code strings
Use these exact displayed reason-code strings in the case card:
- `Unexpected device login succeeded on vendor contractor account`
- `Active VPN session remains live`
- `Badge B-1842 maps to John Mercer`
- `After-hours badge use at South Service Entrance SE-3`
- `Officer report in adjacent Imaging Service Corridor within seven minutes`
- `No escort observed`
- `No linked on-campus evidence yet`
- `Contractor schedule not yet confirmed`
- `Remote session legitimacy not yet confirmed`

### Exact escalation recommendation
`Notify protective services leadership and SOC now.`

## 12. UI contract

### Exact case-card fields for the demo
The case card must contain these fields:
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

### Recommended locked values in the gold scenario
- **case title:** `VendorCo contractor remote-access anomaly with potential on-campus linkage`
- **location:** `South Service Entrance SE-3 / Imaging Service Corridor`
- **primary subject:** `John Mercer (VendorCo biomedical contractor)`
- **trigger summary:** `Successful VPN login from a new device while the remote session remains active.`
- **escalation recommendation when state = Escalate Now:** `Notify protective services leadership and SOC now.`
