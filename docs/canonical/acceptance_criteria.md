# Acceptance Criteria

## Rule zero
The MVP must pass the core acceptance criteria even when OSINT is disabled.

## Core MVP acceptance criteria

### Case opening and linkage
- The system accepts only the locked trigger type.
- The case is opened upstream by SOC or identity tooling, not manually by the duty manager.
- Event 1 alone opens the case in **Observe**.
- Event 2 upgrades the same case to **Verify Now**.
- Event 3 upgrades the same case to **Escalate Now**.
- Escalation is impossible before Event 3.

### Deterministic logic
- Identity resolution from `jmercer@vendorco` to `John Mercer` is deterministic.
- Badge resolution from `B-1842` to `John Mercer` is deterministic.
- Door-to-zone mapping for `SE-3` is deterministic.
- Zone adjacency between `Z-SOUTH-SERVICE-ENTRANCE` and `Z-IMAGING-CORRIDOR` is deterministic.
- Next-action selection follows the locked priority order only.
- AI is not required for state progression, linkage, or next-action selection.

### Exact strings and visible outputs
- The exact reason-code strings display in the expected states.
- The exact next-action strings display in the expected states.
- The escalation recommendation appears only in **Escalate Now**.
- The first screen is the active case card.
- The visible fields match the locked UI contract.
- Provenance is shown for every visible evidence item.

## Expected event-by-event results

| Injection | Input | Expected state | Expected next action | Escalation allowed |
|---|---|---|---|---|
| 1 | `CY-0213-001` | **Observe** | `Call the SOC now to confirm whether the active VPN session for jmercer@vendorco is still live and whether the MFA approval was legitimate.` | No |
| 2 | `AC-0224-001` | **Verify Now** | `Call the VendorCo night supervisor now to confirm whether John Mercer is scheduled onsite and carrying badge B-1842.` | No |
| 3 | `IR-0231-001` | **Escalate Now** | `Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.` | Yes |
