# Adaptive ACO — 0.9.0

ACO 0.9 adds a **shadow adaptation layer** above the Goal Graph and Autonomy Engine.
It turns explicit corrections, preferences and observed outcomes into structured evidence,
but it does **not** let feedback rewrite production policy directly.

## Safety model

The production path remains the deterministic 0.8 stack. Adaptive ACO operates beside it:

`feedback → scoped ledger → candidate proposal → shadow comparison → benchmark → explicit promotion review`

The following invariants are mandatory:

1. **Scope-bound learning.** Feedback belongs to one `scope_id`; evidence from another private scope cannot influence a candidate.
2. **No hidden-reasoning capture.** Feedback records must not contain chain-of-thought, hidden reasoning, scratchpads or equivalent fields.
3. **Append-only evidence semantics.** A ledger is a SHA-256 hash chain. Editing or reordering a prior record invalidates the ledger.
4. **Minimum evidence.** One correction does not become a policy. Candidate proposals require repeated support and minimum consensus.
5. **Shadow first.** Candidates have `state: shadow_only`; they can be evaluated but cannot alter the production Goal Graph score or permission policy.
6. **Bounded ranking deltas.** Learned Goal Graph feature weights are capped by policy.
7. **No permission learning.** Feedback cannot learn away approval, privacy, verification, reconciliation or capability gates.
8. **Promotion is separate.** Promotion requires an exact candidate hash, a frozen benchmark result, historical regressions passing, an explicit approval reference and a rollback reference.
9. **No self-write.** `promotion-check` returns eligibility only. It never edits policy files or activates a candidate.
10. **Rollback remains possible.** Every promotable candidate names the baseline and rollback reference that would restore prior behavior.

## Feedback types

ACO can record evidence about routing, context, Goal Graph ranking, autonomy behavior and output preferences. In 0.9 only two classes can produce adaptive candidates:

- **Output preference** — repeated agreement on a scoped key/value preference.
- **Goal ranking** — repeated evidence that a declared `adaptive_feature` should receive a small positive or negative shadow score delta.

Routing, context and autonomy feedback are retained as structured evidence for future evaluation, but 0.9 does not auto-generate production policy changes from them.

## Shadow ranking

Tasks may declare `adaptive_features`, for example `low_context_cost` or `continuation_value`.
The base Goal Graph score is calculated exactly as in 0.8. Shadow candidates then add bounded deltas only to the comparison result. The graph is not mutated and the base ordering is always returned alongside the shadow ordering.

## Promotion contract

A candidate is only *eligible for promotion* when all configured gates pass. Eligibility is not activation. A host or maintainer must still make a deliberate versioned policy change, rerun release validation and preserve the rollback reference.
