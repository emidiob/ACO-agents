# ACO architecture — v0.7.0

ACO is organized around **selective loading**, not a giant always-on prompt.

```text
natural request
    ↓
Concierge resolves scope + office
    ↓
minimum authorized context
    ↓
selected role method
    ↓
only relevant playbook / optional resource
    ↓
execute with real available tools
    ↓
verification appropriate to the domain
    ↓
compact durable update only if materially useful
```

## 1. Role files stay independently safe

Each of the 363 canonical roles carries a short **ACO ROLE BOOTSTRAP** covering scope, authority, truthful action states, minimum-context retrieval and Compact Memory. This stays inside every role because a native host may load one role without first loading the Concierge.

The long common contracts are no longer copied into every role. Detailed rules live once in shared protocols:

- `OPERATING-CONTRACT.md` — scope, authority, tools, evidence and persistence;
- `CONTEXT-RETRIEVAL.md` — progressive retrieval and blind-review boundaries;
- `PLANNING-AND-APPROVAL.md` — small-task direct action vs substantial planning, and plan ≠ permission;
- `VERIFICATION.md` — prepared/executed/checked/reviewed evidence ladder;
- `COMPACT-MEMORY.md` — pipeline ≠ entity and file-waste controls;
- `LEARNING-AND-SCOPE.md` — scoped lessons without cross-client contamination;
- `ROLE-MAINTENANCE.md` — keep/improve/update/merge/retire maintenance method.

This reduces canonical role Markdown from about 3.10M characters in 0.6.0 to about 1.66M in 0.6.1. That is source/package duplication, not a claim that a live host loaded all roles simultaneously.

## 2. Structured role contracts and advisory routing

Every canonical role also has a generated machine-readable contract in `config/role-contracts.json`. It exposes purpose, `use_when`, `avoid_when`, expected inputs/outputs, method, verification and escalation without replacing the specialist Markdown source.

The local router follows a two-stage pattern:

```text
task text
  → office boundary evidence
  → candidate role evidence
  → smallest useful team (normally 1–3 roles)
  → Concierge / human may accept, refine or override
```

`route-suggest` is advisory and side-effect free. It never grants account access, authorizes a send, expands private scope or proves that a tool exists. Ambiguous requests may fall back to the Concierge for a decisive question. Routing examples are generic package data, not private user memory.

The packaged final routing holdout is deliberately excluded from the consumed example set. Release validation checks both that isolation and the deterministic score gate. The benchmark measures this router on these cases only; it is not proof of universal language understanding.

## 3. Progressive context retrieval

ACO starts from the brief, supplied files and the smallest relevant canonical section. It then identifies material gaps and retrieves only what is needed to close them. It does not silently broaden client, organization or project scope because more data exists.

A few focused refinement cycles are preferable to loading whole histories. If the missing fact remains decisive, ask; if it is nonblocking, label the limitation or reversible assumption.

`BLIND` prevents additional private retrieval. `BLIND-FIRST` delays broader context until the first pass is complete. A clean session/runtime is required for truly independent review when prior context is already visible.

## 4. Verification is domain-specific

ACO distinguishes:

```text
prepared → executed → checked → reviewed
```

Deterministic checks should be used when they answer the question: builds, tests, hashes, dimensions, arithmetic, required fields, frame counts or delivery specifications.

They must not be used as fake proof of subjective quality. A successful build does not prove web design quality; a valid video file does not prove directing/editing quality; a completed application does not prove opportunity fit. Rendered evidence and human/specialist review remain necessary where appropriate.

## 5. Planning does not authorize action

A substantial plan can identify sends, purchases, deletes, migrations, publications or deployments. It cannot authorize them. Consequential execution still needs the relevant scoped human/host permission.

Small reversible requests should not be inflated into multi-office plans.

## 6. Compact Memory remains the single continuity model

ACO v0.7.0 does not add a second memory vault. Ideas, applications, leads, proposals and rejections remain inline pipeline items unless real commitment plus independence/complexity/confidentiality justifies a separate record.

A correction or lesson is not a new Drive file. Durable scoped preferences update the existing canonical document. ACO-wide instructions change only during reviewed library maintenance.

## 7. Scoped learning

Useful corrections can be captured as candidate lessons with the narrowest valid scope:

```text
task/session
→ project/client
→ organization/practice
→ ACO-wide only after reviewed repeated evidence
```

No raw transcript ingestion, background observer or automatic promotion is required. Private client taste never becomes a universal rule merely because it occurred once.

## 8. Maintenance instead of persona inflation

Before adding a role, ask whether the gap is actually:

- a missing capability;
- a shallow method;
- a stale tool/source reference;
- a routing problem;
- or true role-level specialization.

`role-stocktake` is read-only and surfaces review candidates. Merge/Retire decisions remain explicit maintainer decisions.

## 9. Behavioral evals

`config/evals.json` contains representative cross-office behavior cases. The CLI can validate and display them, but it does not run a model. Baseline/candidate comparisons should use equivalent context, host, model and tools; human review is explicitly required for artistic, visual and strategic judgments.

See [EVALS.md](EVALS.md).

## External architectural reference

During the 0.6.1 review, ACO examined the public `affaan-m/ECC` repository for general ideas around progressive retrieval, context budgeting, skill stocktakes, eval-driven verification and scoped continuous learning. ACO does not bundle ECC, require its runtime, copy its agent library or adopt its memory vault. The source review is documented in `research/ECC-ARCHITECTURE-REVIEW.md`.

## 10. Execution & Integration layer — v0.7.0

ACO's domain expertise and its execution capability are intentionally separate.

```text
request
  → office / specialist routing
  → progressive context
  → plan or direct bounded work
  → capability resolution
  → permission / approval check
  → host adapter call (only in an authorized host)
  → execution receipt
  → reconciliation / verification
  → compact durable update only if material
```

### Capability is not knowledge
`LEARNED_SKILL` and `REFERENCE` describe knowledge. `OPTIONAL_TOOL` describes a candidate resource. Only a verified `CONNECTED_INTEGRATION` or `LOCAL_RUNTIME` can satisfy an execution capability, and even then the exact operation must be available and authorized.

### Host adapter boundary
ACO does not ship a credential broker or mandatory integration runtime. A host may map ACO capability IDs to native tools, connected apps, MCP servers, local runtimes or APIs. `config/adapter-contract.json` defines what metadata must be explicit; actual credentials remain in the host/provider boundary.

### Permission boundary
`config/permission-policy.json` distinguishes ordinary read/draft/reversible work from consequential sharing, sending, publishing, applying, deploying, deleting, purchasing and signing. Consequential approval is bound to the SHA-256 of the exact action packet so a materially changed target/payload is not silently covered by an older approval.

### Receipt boundary
The strongest status ACO may report is limited by the actual adapter/provider evidence. A timeout or unknown result is not a failure and not a success; it is `unknown` until reconciled. Unknown exact actions are not retried blindly.

### Workflow state is compact
Workflow states are runtime/coordination facts, not automatic entities or permanent log files. They can remain in chat or an existing compact record. The v0.7 state validator enforces evidence for stronger completion claims and reconciliation after unknown execution outcomes.

### Observability without hidden reasoning
`execution-summary` reports task scope, observable actions, receipt status/evidence, created files, checks, unresolved receipts and next action. It is deliberately not a chain-of-thought or internal deliberation transcript.
