# Progressive context retrieval

Use this when the selected role needs private/project context or a large code/document corpus. The goal is enough evidence to do the job—not maximum retrieval.

## 0. Lock scope
Identify the authorized owner / organization / client / project and permitted sources. Never solve missing context by silently widening scope. If the correct scope is ambiguous and materially changes the answer, ask.

## 1. First pass: smallest useful set
Start with the brief, directly supplied files, the current canonical ACO section, and the one or two sources most likely to answer the task. For a code task, inspect repository instructions and the files closest to the requested change before searching broadly.

## 2. Evaluate gaps
After the first pass, state internally what is still missing:
- a fact required for correctness;
- a constraint required for execution;
- a relationship / decision required for continuity;
- a source required to verify a current claim;
- or no material gap.

Do not fetch more just because more context exists.

## 3. Refine, at most a few cycles
Search specifically for the missing item using terminology discovered in the first pass. Prefer direct sources over summaries. Two or three focused refinement cycles are normally enough; if the gap remains unresolved, ask the user or proceed with an explicit limitation rather than reading everything.

## 4. Stop at sufficient context
Stop when the remaining uncertainty does not change the deliverable. More retrieval has a cost: privacy exposure, contradictory stale history, context-window pressure and slower execution.

## Blind / independent review
`BLIND` means no additional private retrieval. `BLIND-FIRST` means complete a first pass from the supplied material before loading broader context. Because an existing runtime cannot unsee material already present, use a clean session / delegated context for a genuinely independent critique.

## Cross-client and cross-project rules
- Never search another client / organization to fill a gap unless the user explicitly authorizes that comparison.
- Shared public methods may cross scopes; private facts, drafts, contacts, pricing, files and preferences may not.
- A memory hit is evidence, not permission and not necessarily current. Verify important current state against the authoritative source.
