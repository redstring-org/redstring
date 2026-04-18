# Architecture Rationale

This document explains **why** the MVP is built the way it is. It is a supporting rationale document only. If this file conflicts with `prd_v1_2_osint_update.md`, the PRD wins.

## 1. Architecture recommendation

Build a **deterministic cross-domain case engine** that opens from one qualifying cyber trigger, enriches the case with deterministic badge and suspicious-person correlation, and renders a single explainable case card for one Hospital Security Duty Manager.

## 2. Why this architecture is correct for the MVP

### One operator, one decision, one workflow
The MVP is designed around one decision bottleneck: whether a suspicious vendor remote-access anomaly has become a campus incident that needs immediate operational follow-up. A narrow case-first workflow is stronger than a broad dashboard because it gives the operator one actionable answer instead of a pile of disconnected signals.

### Deterministic core, AI explanation layer
The product must be trusted by operators and legible to judges. That requires event normalization, identity mapping, door-zone mapping, time-window checks, state transitions, and next-action selection to be deterministic and auditable. AI is used only after the case is fully assembled, and only to phrase grounded content from structured case JSON.

### Case-first UX over platform UX
A queue-first or map-first product forces the team to build a platform instead of a demoable decision tool. The MVP should open directly on the active case card because the demo is about one incident path and one escalation decision, not broad monitoring.

### Why optional OSINT stays constrained
OSINT is useful as contextual reinforcement, but it is not reliable enough to be part of the core escalation logic for the MVP. Keeping it optional, provenance-preserving, and collapsed by default protects trust and prevents the demo from depending on noisier data.

## 3. Layer-by-layer rationale

### Ingest layer
Purpose: receive the upstream cyber trigger and collect candidate cross-domain events.

Why this matters:
- keeps source provenance intact
- makes every downstream claim traceable to a real event
- allows the system to stay operational even when AI is disabled

MVP rule:
- ingest only the locked feeds needed for the gold scenario

### Normalization layer
Purpose: convert heterogeneous events into one canonical event model.

Why this matters:
- makes test data stable
- makes rule evaluation reproducible
- keeps the UI and explanation layer grounded in a consistent schema

MVP rule:
- use strict deterministic schema mapping
- reject malformed or low-quality events instead of guessing

### Correlation / rules layer
Purpose: link the cyber trigger to the mapped badge event and suspicious-person report.

Why this matters:
- this is where product trust is won or lost
- every match must be explainable using fixed mapping and time/zone rules
- the operator needs to see why events were linked and why some facts still weaken the case

MVP rule:
- exact identity resolution through contractor and badge mappings
- exact time-window checks
- exact door-zone and adjacency checks

### State engine
Purpose: convert the linked evidence pattern into one operator-facing state.

Why this matters:
- the duty manager should not interpret raw evidence manually
- the product promise is not “interesting data,” it is “clear decision state”

MVP rule:
- `Observe`, `Verify Now`, and `Escalate Now` must be deterministic outputs only
- escalation is not allowed until the suspicious-person report is linked

### Next-action layer
Purpose: choose the single human check that most reduces uncertainty.

Why this matters:
- operators need one next step, not a menu of options
- a deterministic action matrix keeps the product crisp and credible

MVP rule:
- choose from the locked next-action matrix only
- AI may rewrite the wording only if the meaning is unchanged

### AI explanation layer
Purpose: turn the final structured case into concise operator language.

Why this matters:
- makes the product feel AI-native without becoming a thin LLM wrapper
- reduces reading load while preserving evidence traceability

MVP rule:
- AI may only phrase grounded facts, contradictions, missing evidence, and the selected action
- AI may not correlate, rank, score, or decide
- the product must still work with deterministic template text if AI is unavailable

### Operator UX / case card layer
Purpose: present one assembled case instead of a dashboard of unrelated signals.

Why this matters:
- keeps the demo fast
- keeps the product legible
- reinforces that this is a decision support product, not a monitoring surface

MVP rule:
- first screen is the active case card
- state is visually primary
- next human check is visually secondary
- timeline, why linked, what weakens it, and provenance must be visible

## 4. Why the gold scenario is right

The gold scenario is strong because it demonstrates the full product promise with minimal scope:
- an upstream cyber anomaly alone is not enough to escalate
- on-campus corroboration changes the operator decision
- the product visibly progresses from Observe to Verify Now to Escalate Now
- the final recommendation is concrete and operational

This makes the demo easy to understand in under two minutes and easy to judge on trust, clarity, and usefulness.

## 5. Why this should not expand during build

Expanding the MVP would weaken both execution and demo clarity.

The team should not add:
- more trigger types
- more primary operator flows
- broader dashboards
- model-driven correlation
- model-driven confidence
- OSINT-dependent logic

Each of those additions makes the product less explainable, less demoable, and harder to finish.

## 6. Technical posture for builders

### What must be real
- state transitions
- deterministic rule evaluation
- identity/badge/door/zone mappings
- case assembly
- visible explanation fields
- event injection for the live demo

### What may be mocked or simplified
- upstream SOC source
- access-control source transport
- suspicious-report source transport
- AI phrasing service
- optional OSINT feed

### What must never be faked in the core demo
- state progression logic
- event-to-case linkage logic
- next-action selection
- escalation recommendation timing

## 7. Final build principle

Build the smallest system that can prove this sentence:

**A suspicious vendor remote-access anomaly becomes an actionable hospital incident only when deterministic campus evidence confirms it, and the product makes that escalation decision legible in one case card.**
