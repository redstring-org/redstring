# Demo Contract

## Purpose
Define exactly what the judges must see, what may be hidden, and what must not appear in the MVP demo.

## Core promise
The demo must prove that one deterministic engine turns one cyber trigger plus one badge event plus one suspicious-person report into one clear operational decision for one Hospital Security Duty Manager.

## What the first screen must be
The first screen must be the active gold-scenario case card.

It must not open on:
- an empty queue
- a case list
- a map-first dashboard
- a chat-first surface
- a settings or admin screen

## What must happen live
The presenter must show the case progress live through the locked three-event sequence:
1. cyber trigger -> **Observe**
2. badge event -> **Verify Now**
3. suspicious-person report -> **Escalate Now**

The presenter must show, at minimum:
- the current state
- the next human check
- the timeline
- why linked
- what weakens it
- the escalation recommendation once the case reaches **Escalate Now**

## What judges should understand within 20 seconds
- this is not a generic chatbot
- this is not a broad dashboard platform
- this is one explainable case engine for one operator
- the state progression is deterministic
- AI only phrases grounded outputs from existing case facts

## What can be hidden
The demo may hide:
- raw JSON
- internal IDs
- numeric score
- debug rule traces
- backend plumbing
- empty queue infrastructure
- internal map or graph tooling
- OSINT module if not enabled

## What must not appear
The demo must not show:
- a freeform chat box as the main interaction pattern
- a map as the primary experience
- a queue as the first screen
- multiple alternative trigger types
- a general search surface
- autonomous response controls
- a prominent confidence number or score dial
- OSINT as a primary evidence panel

## Required outcome by the end of the demo
By the end of the main run, the case card must show:
- **Escalate Now**
- `Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.`
- `Notify protective services leadership and SOC now.`

## Optional OSINT rule for the demo
Optional OSINT may be shown only after the core path is already clear.

If shown, it must:
- be collapsed by default
- preserve provenance
- be visually subordinate
- add context only
- not affect the state progression
- not affect the selected next action
- not be required to explain why the case escalates

## Demo fail conditions
The demo fails if the audience could reasonably conclude any of the following:
- the product depends on AI to decide what is happening
- the product needs OSINT to justify escalation
- the product is mainly a dashboard, map, or chatbot
- the product cannot explain why the case moved between states
