# Cyber-Physical Correlation Engine — MVP Build + Demo

This repo contains the locked MVP for a **deterministic cross-domain case engine** built for **one hospital campus** and **one operator: the Hospital Security Duty Manager**.

The product opens from **one qualifying cyber trigger only**, links **one matched badge/access event** and **one suspicious-person report** using deterministic rules, and renders **one active case card** that progresses through **Observe -> Verify Now -> Escalate Now**. AI is allowed only to phrase grounded case content from structured case JSON. It is not allowed to correlate evidence, determine confidence, select actions, or change case state.

## Start here

1. `docs/canonical/prd_v1_2_osint_update.md`
2. `docs/canonical/gold_scenario.md`
3. `docs/canonical/acceptance_criteria.md`
4. `docs/canonical/ui_contract.md`
5. `docs/canonical/data_contract_and_seed_spec.md`
6. `docs/build/build_project_instructions.md`
7. `docs/build/event_injection_runbook.md`
8. `docs/build/demo_contract.md`

## Repo intent

This is not a broad platform build. It is a narrow demoable MVP with one gold scenario and one clear escalation decision.

### Locked product shape
- one hospital campus
- one operator: Hospital Security Duty Manager
- one qualifying cyber trigger only
- one matched badge/access event
- one suspicious-person report
- one active case card
- deterministic `Observe -> Verify Now -> Escalate Now`
- deterministic next-action matrix
- AI only for grounded phrasing
- no chatbot
- no queue-first UI
- no map-first UI
- optional OSINT only as contextual evidence

## Canonical docs

### Core deterministic demo
- `docs/canonical/prd_v1_2_osint_update.md`
- `docs/canonical/gold_scenario.md`
- `docs/canonical/acceptance_criteria.md`
- `docs/canonical/ui_contract.md`
- `docs/canonical/data_contract_and_seed_spec.md`
- `docs/build/build_project_instructions.md`
- `docs/build/event_injection_runbook.md`
- `docs/build/demo_contract.md`

### Optional OSINT support
- `docs/optional/osint_contract.md`
- `docs/optional/osint_enablement_note.md`

### Supporting rationale only
- `docs/reference/architecture_rationale.md`
- `docs/reference/ai_native_strategy_and_mvp_architecture.md`
- `docs/reference/persona_and_workflow_selection.md`
- `docs/reference/problem_framing_jtbd.md`
- `docs/reference/trend_scan_and_wedge_recommendation.md`
- `docs/reference/brutal_prd_critique.md`

## What “done” means

The MVP is done only when the locked gold scenario runs end to end and the acceptance criteria pass exactly.

That means:
- Event 1 opens the case in **Observe**
- Event 2 upgrades the same case to **Verify Now**
- Event 3 upgrades the same case to **Escalate Now**
- the exact reason-code strings appear
- the exact next-action strings appear
- the escalation recommendation appears only in **Escalate Now**
- the first screen is the active case card
- the core MVP passes with OSINT disabled

## Build guardrails

Do not change:
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

## Suggested repo layout

```text
/docs
  /canonical
    prd_v1_2_osint_update.md
    gold_scenario.md
    acceptance_criteria.md
    ui_contract.md
    data_contract_and_seed_spec.md
  /build
    build_project_instructions.md
    event_injection_runbook.md
    demo_contract.md
  /optional
    osint_contract.md
    osint_enablement_note.md
  /reference
    architecture_rationale.md
    ai_native_strategy_and_mvp_architecture.md
    persona_and_workflow_selection.md
    problem_framing_jtbd.md
    trend_scan_and_wedge_recommendation.md
    brutal_prd_critique.md
```

## One-line explanation for judges

A deterministic engine turns one cyber trigger plus one badge event plus one suspicious-person report into one clear verify-or-escalate decision, while AI only explains the already-assembled case.
