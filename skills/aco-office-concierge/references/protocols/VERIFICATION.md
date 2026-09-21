# Verification and evidence

ACO should finish with the strongest verification the domain and available tools can actually support. Verification is not a generic "looks good" statement.

## Before substantial execution
Define what success means at the level appropriate to the task. Small tasks may need one check; substantial tasks should have explicit acceptance criteria before expensive or irreversible work.

## Evidence ladder
1. **Prepared** — a plan, draft, prompt, command or artifact exists.
2. **Executed** — the relevant tool/action actually ran or the artifact was actually created.
3. **Checked** — deterministic or observable checks were performed on the result.
4. **Reviewed** — a human or appropriate specialist reviewed dimensions that cannot be proven mechanically.

Do not skip levels in status language.

## Prefer deterministic checks when they answer the question
Examples: build exit code, tests, schema validation, file hashes, dimensions, frame counts, link checks, arithmetic, required fields, delivery specs. Record the actual command/tool and outcome.

## Do not use deterministic checks to fake subjective proof
- A successful frontend build does not prove a visually strong website.
- A valid video file does not prove good editing, directing or continuity.
- A spellcheck does not prove good writing.
- A completed application form does not prove strategic fit.
- An agent score does not replace artist / curator / client judgment.

Use rendered/browser/media evidence and human review where appropriate.

## Failure and uncertainty
A failed check blocks a claim that depends on it. An unrun check stays unrun. If the environment prevents verification, report the exact limitation and leave the work **ready for review**, not "verified".

## External actions
For sends, bookings, publishing, payments and remote writes, provider/tool evidence must match the exact target and operation. `accepted`, `queued`, `sent`, `delivered` and `read` are different states. Reconcile unknown outcomes before retrying.
