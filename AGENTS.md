# AGENTS.md

## Purpose
This repo exists to ship one deterministic MVP demo for the Cyber-Physical Correlation Engine.

## Read Order
Read these first and treat them as binding, in this exact order:

1. `docs/canonical/prd_v1_2_osint_update.md`
2. `docs/canonical/gold_scenario.md`
3. `docs/canonical/acceptance_criteria.md`
4. `docs/canonical/ui_contract.md`
5. `docs/canonical/data_contract_and_seed_spec.md`
6. `docs/build/build_project_instructions.md`
7. `docs/build/event_injection_runbook.md`
8. `docs/build/demo_contract.md`

If any of those canonical paths are absent in the current checkout, use the matching file in `mvp_build_demo_markdown_pack_v3/` only as a temporary fallback, and restore the canonical path before merge.

## Locked MVP Shape
Build exactly this:
- one hospital campus
- one operator: Hospital Security Duty Manager
- one qualifying cyber trigger only
- one matched badge/access event
- one suspicious-person report
- one active case only
- one active case card
- deterministic `Observe -> Verify Now -> Escalate Now`
- deterministic next-action matrix
- AI only for grounded phrasing
- no chatbot
- no queue-first UI
- no map-first UI

## Deterministic Boundary
Deterministic only:
- case opening
- schema mapping
- identity matching
- badgeholder mapping
- door-to-zone mapping
- zone adjacency checks
- time-window logic
- state transitions
- next-action selection
- escalation gates

AI may only:
- explain grounded facts
- phrase deterministic reason codes
- phrase contradictions and missing evidence
- phrase the already-selected next human check

AI must not:
- determine correlation
- determine confidence state
- select the next action
- invent facts or identities

## No-Change Rules
Do not change:
- operator
- campus scope
- trigger type
- the three-event gold scenario
- state progression
- next-action strings
- reason-code strings
- escalation recommendation
- AI boundary
- first-screen UI shape
- optional-only status of OSINT

Do not add:
- a second trigger type
- a second primary incident path
- queue-first home screen
- map-first home screen
- chat-first workflow
- autonomous response
- model-driven correlation
- model-driven confidence
- OSINT-driven escalation path

## Working Rules
- Prefer the smallest safe fix that keeps the gold scenario working.
- Keep backend work in the current checked-in Python paths unless the repo is being intentionally reorganized: `backend/app/`, `backend/tests/`, and `data/fixtures/`.
- Verify the deterministic backend path before merge with:
  - `cd backend && /home/f1k/dev/play/redstring/.venv/bin/python -m pytest -q`
