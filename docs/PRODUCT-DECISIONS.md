# Product decisions — 0.6.2

## Goal

Make ACO more reliable by improving **selection, handoff and evidence discipline**, not by increasing the number of personas. 0.6.2 keeps 363 roles, 16 entry skills, 61 workflows, 97 optional resources and Compact Memory.

## Routing before persona expansion

A role gap may actually be a routing problem, a shallow method, stale source/tool information or a missing capability. The release therefore adds structured contracts for every role and an advisory two-stage office/role router. Normal output is the smallest useful team, usually one specialist and at most three roles. Ambiguous requests may return to the Concierge.

The router never authorizes a send, purchase, submission, destructive change or private-context expansion. It is deterministic local package logic, not a background agent.

## Holdout discipline

Development examples may improve the router, but final validation must remain unseen. The 28-case final holdout is excluded from `routing-examples.json`; routing was frozen before that holdout was run. The release scored 98.57/100 with zero critical failures. Future tuning after seeing a final-holdout failure requires a new unseen holdout.

## Role contracts, not duplicate role prose

Machine-readable contracts expose each role's office, purpose, use/avoid conditions, inputs, outputs, method, verification and escalation. They are generated from canonical ACO sources and help routing/maintenance; they do not replace the specialist Markdown or create a second editable role catalogue.

## Handoffs and capability truth

A compact handoff records task, owner, state, decisions, evidence, unknowns and next action. Checked/reviewed claims require evidence. Capability state explicitly separates availability, authorization and verification. A registry entry, PATH result or app name is never treated as permission or execution proof.

## Evaluation is layered

Automatic tests validate package behavior. The routing holdout validates deterministic selection on known cases. A 24-case structured behavioral simulation provides same-model regression evidence and scored 97.83/100 with zero critical failures. Open-ended artistic, curatorial, brand, design, writing and legal quality still needs real evidence and appropriate human/professional review.

## Compact Memory remains the continuity model

No new memory vault, transcript harvester or file-per-lesson system is introduced. Ideas, leads, applications, proposals and rejections remain compact pipeline items until real commitment and justified independence/complexity/confidentiality warrant a separate record.

## External resources remain optional

The 97-resource registry is not a capability list. A task should use zero or a few relevant resources. External software is not bundled or installed automatically; licensing, source/version, data destination, cost and actual host capability must be checked when operational use matters.

## Release boundary

One complete 0.6.2 ZIP and checksum define the release. Updating GitHub, a local ACO installation or private Drive knowledge are separate actions. The proprietary ACO LICENSE remains unchanged.
