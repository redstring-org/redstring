# Demo Seed Pack — Scenario 01

This folder contains a small, hackathon-friendly seed dataset for a cyber-physical correlation demo.

## What is included

- `badge_events.csv`
- `suspicious_person_reports.csv`
- `osint_posts.csv`
- `scenario_manifest.json`

## Recommended use

Use these as static seed files for local development, demo playback, or scripted event injection.

### Best default team workflow

1. Create a folder in your repo:
   - `demo_data/scenario_01/`

2. Commit these files into Git.
   This is the easiest way to keep everyone on the same scenario and avoid version confusion.

3. Load them in one of two ways:
   - **Fastest**: your backend reads the CSVs directly on startup
   - **Better demo**: a small injector script replays rows in timestamp order with a speed multiplier

4. Keep one manifest file per scenario so the team knows:
   - what story the data is telling
   - which alert should fire
   - which event(s) are background noise vs signal

## Why CSV is the right format for a hackathon

- easy to inspect manually
- easy to edit in Excel, Google Sheets, or VS Code
- easy to parse in Python
- easy to diff in Git
- no database setup required

## Suggested repo structure

```text
/demo_data
  /scenario_01
    badge_events.csv
    suspicious_person_reports.csv
    osint_posts.csv
    scenario_manifest.json
/docs
  demo_runbook.md
/scripts
  replay_scenario.py
```

## Team sharing recommendation

Best option:
- store this in your shared GitHub repo
- use pull requests for scenario edits
- pin one scenario as the “judge demo” scenario

Good backup option:
- also upload the folder to shared Google Drive for non-technical teammates to review and edit

## Next improvement

After this seed pack, create:
- `scenario_02_false_positive.csv set`
- `scenario_03_higher_confidence_escalation.csv set`

That gives you one clean positive case, one noisy case, and one stronger escalation case for demos and judging.
