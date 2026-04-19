# PLANS.md

## Mission
Ship one deterministic MVP demo for the locked gold scenario, starting with the Python/FastAPI backend and preserving the exact contract-defined state progression and strings.

## Current Decisions
- Backend only until the canonical docs are restored and stable.
- Python + FastAPI is the active implementation path.
- The current backend lives in `backend/app/`.
- Deterministic fixtures live in `data/fixtures/`.
- The backend acceptance path lives in `backend/tests/`.
- OSINT remains optional, off by default, and never state-driving.

## Ordered Plan
1. Restore the binding docs to `docs/canonical/` and `docs/build/` with the same contents as the markdown pack.
2. Keep the backend deterministic and limited to the locked gold scenario.
3. Preserve the current API surface only:
   - `GET /health`
   - `GET /api/case/active`
   - `POST /api/demo/inject`
   - `POST /api/demo/reset`
4. Keep the fixture set limited to the gold scenario and reference mappings already defined in the contract.
5. Keep one stable backend acceptance path green:
   - `cd backend && /home/f1k/dev/play/redstring/.venv/bin/python -m pytest -q`
6. Do not take frontend, map, queue, chat, or second-scenario work until the backend contract and docs are fully locked.

## Acceptance Gate
The current slice is only done when:
- Event 1 -> `Observe`
- Event 2 -> `Verify Now`
- Event 3 -> `Escalate Now`
- exact next-action strings match the contract
- exact escalation recommendation appears only in `Escalate Now`
- OSINT is not required for the core path
- the backend test command passes cleanly

## Deferred Until After This Slice
- frontend restoration
- canonical repo-shape cleanup beyond the smallest safe fix
- optional OSINT display work
- non-demo infrastructure
- any additional trigger types or incident paths
