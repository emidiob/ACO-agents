# Execution, capabilities and consequential actions

ACO separates **knowledge**, **availability**, **authorization**, **execution** and **verification**. A role knowing how to do something never proves the host can do it.

## Capability states
Use the narrowest accurate state:

- `LEARNED_SKILL` — ACO knows a method; no external capability is implied.
- `REFERENCE` — a source can inform work; it cannot perform an action.
- `OPTIONAL_TOOL` — a candidate tool exists but is not execution-ready merely because it is in the registry.
- `CONNECTED_INTEGRATION` — a host/service connection is present; exact operations, authorization and evidence still need verification.
- `LOCAL_RUNTIME` — a local executable/runtime is present; presence alone is not proof a command succeeded.
- `UNAVAILABLE` — the capability is not available in this environment.
- `BLOCKED` — the capability may exist but current authorization/policy prevents use.

Before a consequential action, resolve the exact capability and operation against actual host evidence. If it is not ready, use the declared fallback and label the external action accurately as not executed.

## Permission levels
ACO uses `READ`, `DRAFT`, `PREVIEW`, `WRITE`, `SHARE`, `SEND`, `PUBLISH`, `APPLY`, `DEPLOY`, `DELETE`, `PURCHASE` and `SIGN`.

`READ`, `DRAFT` and bounded reversible work do not need repetitive approvals when already inside the user's explicit task scope. Sharing/access changes, external sends, public publication, applications, production deployment, deletion, purchases and signing require exact scoped approval at the consequential step. Approval binds to the final action packet; a general plan or earlier draft is not enough.

Host/system permission controls always take precedence. ACO's policy narrows intended behavior but cannot grant provider access.

## Execution lifecycle

```text
request
→ route specialist
→ prepare action packet
→ resolve capability
→ check permission / approval
→ execute through an actual host adapter
→ capture receipt
→ reconcile ambiguous outcomes
→ verify the strongest supported claim
→ update compact continuity only when durable
```

The local CLI's `execution-plan` stops before the adapter call. It is a readiness decision, not an executor.

## Retry discipline
An exact action with an `unknown` or in-flight result must be reconciled before retrying. An exact action with positive execution evidence should be inspected rather than repeated. This prevents duplicate messages, posts, submissions, payments or remote writes.

## Receipts
Consequential outcomes need evidence that identifies the exact capability/operation and provider or artifact result. `accepted`, `queued`, `sent`, `delivered`, `read`, `published`, `submitted`, `deployed`, `purchased` and `signed` are not interchangeable.

Use [ADAPTERS-AND-RECEIPTS.md](ADAPTERS-AND-RECEIPTS.md) and [WORKFLOW-STATE.md](WORKFLOW-STATE.md) for the detailed host contract.
