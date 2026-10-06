# Adaptive feedback and shadow learning

Use this protocol only when the user has supplied an explicit correction, preference or observable outcome that could improve future ACO decisions.

## Rules

1. Record **structured evidence**, not hidden chain-of-thought or private scratchpads.
2. Keep feedback inside the current authorized `scope_id`; never aggregate a private client/entity into another scope.
3. A single correction is evidence, not a new policy.
4. Repeated evidence may produce a **shadow-only candidate** when the configured support/consensus threshold is met.
5. Shadow candidates may compare behavior, but must not change routing, permissions, privacy rules, approval rules or production Goal Graph scoring by themselves.
6. Never infer permission from preference. A user preferring fewer confirmations does not waive approval gates.
7. Promotion requires an exact candidate hash, frozen benchmark evidence, historical regressions passing, explicit approval and a rollback reference.
8. `promotion-check` is advisory. Activation is a separate versioned maintainer action followed by full release validation.

## What 0.9 can adapt

- scoped output preferences represented as repeated key/value evidence;
- bounded Goal Graph `adaptive_feature` ranking deltas evaluated in shadow mode.

Routing, context and autonomy feedback can be recorded for evaluation but do not auto-generate production policy changes in 0.9.
