# MVP Build + Demo Project Instructions

Treat `prd_v1_2_osint_update.md` as the only source of truth. Do not reopen wedge selection, persona selection, broad strategy, trigger selection, or the main product shape.

## Build exactly this
- one hospital campus
- one operator: Hospital Security Duty Manager
- one qualifying cyber trigger only
- one matched badge/access event
- one suspicious-person report
- one active case card
- deterministic **Observe -> Verify Now -> Escalate Now**
- deterministic next-action matrix
- AI only for grounded phrasing
- no chatbot
- no queue-first UI
- no map-first UI

## Build objective
Deliver a deterministic active case card that opens from one upstream cyber trigger, links the badge and suspicious-person evidence using fixed rules, and shows the exact state, reason codes, next human check, and escalation recommendation defined in the canonical PRD.

## What the team must not change
- the operator
- the campus scope
- the trigger type
- the three-event gold scenario
- the state progression
- the next-action strings
- the reason-code strings
- the escalation recommendation
- the AI boundary
- the first-screen UI shape
- the optional-only status of OSINT

## Hard implementation rules
1. Case opening is deterministic.
2. Identity mapping is deterministic.
3. Door-zone mapping is deterministic.
4. Time-window checks are deterministic.
5. State transitions are deterministic.
6. Next-action selection is deterministic.
7. AI does not correlate, score, or decide.
8. The product still works if AI phrasing is disabled.
9. The core MVP must pass with OSINT disabled.
10. OSINT, if enabled, is contextual only.

## UI rules
- The first screen must be the active case card.
- State is visually primary.
- Next human check is visually secondary.
- Timeline, why linked, what weakens it, and provenance must be visible.
- Numeric score must be hidden or visually secondary.
- OSINT must be collapsed by default if present.

## Forbidden drift
Do not add:
- a second trigger type
- a second incident path for the primary demo
- autonomous response
- model-driven correlation
- model-driven confidence
- a queue-first home screen
- a map-first home screen
- a chat-first workflow
- an OSINT-driven escalation path

## Delivery bar
The MVP is not done when the UI looks plausible. It is done when the locked gold scenario runs end to end and the acceptance criteria pass exactly.
