# Gold Scenario

## Purpose
This is the single incident path the MVP Build + Demo project must implement first. Do not improvise alternate incidents until this one works end to end.

## Trigger
`02:13 AM — jmercer@vendorco successful VPN login from a new device while the remote session remains active.`

## Badge event
`02:24 AM — badge B-1842 used at South Service Entrance SE-3 after hours.`

## Suspicious-person report
`02:31 AM — officer report: male in VendorCo jacket moving two equipment cases toward Imaging Service Corridor; no escort observed.`

## Optional OSINT example
Example only: a public post or forum item mentioning unusual vendor activity or equipment movement near the same hospital service entrance in the same time window.

### Allowed role of OSINT
- contextual reinforcement only
- provenance-preserving
- collapsed by default
- not required in the gold demo
- cannot open the case by itself
- cannot change state by itself
- cannot justify escalation by itself

## State progression
- Event 1 -> **Observe**
- Event 2 -> **Verify Now**
- Event 3 -> **Escalate Now**

## Exact next-action strings
### Observe
`Call the SOC now to confirm whether the active VPN session for jmercer@vendorco is still live and whether the MFA approval was legitimate.`

### Verify Now
`Call the VendorCo night supervisor now to confirm whether John Mercer is scheduled onsite and carrying badge B-1842.`

### Escalate Now
`Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.`

## Escalation recommendation
`Notify protective services leadership and SOC now.`

## Exact reason-code strings
- `Unexpected device login succeeded on vendor contractor account`
- `Active VPN session remains live`
- `Badge B-1842 maps to John Mercer`
- `After-hours badge use at South Service Entrance SE-3`
- `Officer report in adjacent Imaging Service Corridor within seven minutes`
- `No escort observed`
- `No linked on-campus evidence yet`
- `Contractor schedule not yet confirmed`
- `Remote session legitimacy not yet confirmed`

## Key mappings
- `jmercer@vendorco` -> `John Mercer` -> `P-1007`
- `B-1842` -> `P-1007`
- `SE-3` -> `South Service Entrance SE-3` -> `Z-SOUTH-SERVICE-ENTRANCE`
- `Z-SOUTH-SERVICE-ENTRANCE` is one-hop adjacent to `Z-IMAGING-CORRIDOR` in the same building

## Seed payload references
- cyber trigger event -> `CY-0213-001`
- badge event -> `AC-0224-001`
- suspicious-person report -> `IR-0231-001`
- contractor identity -> `P-1007`
- badge mapping -> `B-1842`
- door mapping -> `SE-3`
- zone adjacency -> `Z-SOUTH-SERVICE-ENTRANCE` to `Z-IMAGING-CORRIDOR`

## Build note
The product should be considered broken if this scenario does not produce the exact state progression and exact strings defined above.
