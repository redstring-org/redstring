# OSINT Enablement Note

## Rule zero
The MVP must work completely with OSINT disabled.

## Default mode
For the core build and primary demo run:
- OSINT is disabled or hidden
- no OSINT fetch is required
- no OSINT event is required in seed data
- no OSINT panel is shown on first load

## Enabled mode
If deployment chooses to enable OSINT:
- keep it contextual only
- keep it collapsed by default
- require provenance for every item
- do not allow OSINT to affect state progression
- do not allow OSINT to affect escalation eligibility

## Build implication
OSINT should be implemented behind a clean feature flag or equivalent configuration switch.

Example:
- `ENABLE_OSINT_CONTEXT=false` for the core demo
- `ENABLE_OSINT_CONTEXT=true` for optional secondary demonstration only

## Test implication
Two test passes are required:
1. OSINT disabled -> all core MVP acceptance criteria pass
2. OSINT enabled -> all core MVP acceptance criteria still pass and OSINT remains contextual only

## Anti-drift reminder
If the build starts to depend on OSINT to make the story feel complete, the build has drifted from the locked MVP.
