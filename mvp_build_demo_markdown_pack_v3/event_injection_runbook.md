# Event Injection Runbook

## Purpose
Run the gold demo in a controlled, repeatable sequence that proves the deterministic case engine works end to end.

## Rule zero
Use the locked gold scenario only. Do not improvise alternate events during the primary demo.

## Demo objective
Show one active case card progressing through:
- **Observe**
- **Verify Now**
- **Escalate Now**

## Required environment state before demo
- app is running and reachable
- first screen is the active gold-scenario case card shell
- queue-first UI is hidden or absent
- map-first UI is hidden or absent
- OSINT is disabled by default for the primary run
- deterministic mappings are loaded:
  - `jmercer@vendorco` -> `John Mercer` -> `P-1007`
  - `B-1842` -> `P-1007`
  - `SE-3` -> `South Service Entrance SE-3` -> `Z-SOUTH-SERVICE-ENTRANCE`
  - `Z-SOUTH-SERVICE-ENTRANCE` adjacent to `Z-IMAGING-CORRIDOR`
- exact next-action strings and reason-code strings are present in config or templates

## Required seed objects
- contractor identity record: `P-1007`
- cyber event: `CY-0213-001`
- badge event: `AC-0224-001`
- suspicious-person report: `IR-0231-001`

## Primary live sequence

### Step 1 — Load the first screen
Show the active case card shell with no queue and no chat.

Expected visible elements:
- case title
- location
- state badge area
- timeline area
- why linked area
- what weakens it area
- next human check area
- provenance area

### Step 2 — Inject the cyber trigger
Inject `CY-0213-001`:

`02:13 AM — jmercer@vendorco successful VPN login from a new device while the remote session remains active.`

Expected result:
- state becomes **Observe**
- next action becomes:
  `Call the SOC now to confirm whether the active VPN session for jmercer@vendorco is still live and whether the MFA approval was legitimate.`
- escalation recommendation is not shown
- timeline shows the cyber trigger
- why linked includes:
  - `Unexpected device login succeeded on vendor contractor account`
  - `Active VPN session remains live`
- what weakens it includes:
  - `No linked on-campus evidence yet`
  - `Remote session legitimacy not yet confirmed`

### Step 3 — Inject the badge/access event
Inject `AC-0224-001`:

`02:24 AM — badge B-1842 used at South Service Entrance SE-3 after hours.`

Expected result:
- same case is updated, not a new case
- state becomes **Verify Now**
- next action becomes:
  `Call the VendorCo night supervisor now to confirm whether John Mercer is scheduled onsite and carrying badge B-1842.`
- escalation recommendation is still not shown
- timeline now shows cyber trigger + badge event
- why linked includes:
  - `Badge B-1842 maps to John Mercer`
  - `After-hours badge use at South Service Entrance SE-3`
- what weakens it includes:
  - `Contractor schedule not yet confirmed`

### Step 4 — Inject the suspicious-person report
Inject `IR-0231-001`:

`02:31 AM — officer report: male in VendorCo jacket moving two equipment cases toward Imaging Service Corridor; no escort observed.`

Expected result:
- same case is updated again, not a new case
- state becomes **Escalate Now**
- next action becomes:
  `Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.`
- escalation recommendation appears:
  `Notify protective services leadership and SOC now.`
- timeline now shows all three events
- why linked includes:
  - `Officer report in adjacent Imaging Service Corridor within seven minutes`
  - `No escort observed`

## Optional OSINT demo branch
Use only after the core path succeeds.

### Step 5 — Reveal optional OSINT
If OSINT is enabled, open a collapsed contextual drawer or disclosure element.

Allowed content:
- one provenance-preserving OSINT item tied to the same facility and relevant time window
- source label
- timestamp
- URL or source reference
- location hint

Expected result:
- no state change
- no next-action change
- no escalation-rule change
- OSINT remains visually subordinate to the three core evidence items

## Speaker track by step
- Step 1: `This opens directly on the active case, not a queue.`
- Step 2: `A cyber trigger creates an Observe case, but escalation is not yet allowed.`
- Step 3: `A matched badge event upgrades the same case to Verify Now.`
- Step 4: `A nearby officer report upgrades the case to Escalate Now and gives one concrete action.`
- Step 5 optional: `If configured, OSINT can add context, but it never drives escalation.`

## Demo fail conditions
The demo should be considered failed if any of the following occur:
- the first screen is a queue, map, or chat surface
- Event 2 creates a second case instead of updating the first
- Event 3 fails to move the case to **Escalate Now**
- escalation appears before Event 3
- next-action text differs from the locked strings
- reason-code text differs from the locked strings
- OSINT is required to make the core demo work
- OSINT changes the state by itself

## Reset procedure
After each run:
- clear the active case state
- clear injected events
- preserve deterministic mappings and templates
- confirm OSINT is disabled again before rerunning the primary path
