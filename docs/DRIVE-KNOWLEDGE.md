# Google Drive as ACO's optional private knowledge layer

ACO keeps reusable agent logic public and private knowledge outside the repository.

## Important public-distribution rule

The public ACO plugin is **skills-only**. It does not bundle, publish, or repackage Google Drive. Users who want persistent Drive-backed knowledge connect the official Google Drive app separately and authorize their own account. Installing ACO alone never grants access to Drive.

This separation is intentional:

```text
ACO public plugin
  generic skills + routing + templates
          |
          | optional, separately authorized
          v
Google Drive app
  user's private knowledge + history
```


## User-facing onboarding

ACO may proactively explain the optional Drive workflow when persistent context would materially help:

> **Want ACO to remember your projects, decisions, history, and context across sessions? Connect Google Drive and choose or create a private ACO knowledge folder. Or continue without persistent memory.**

If Drive is connected but an ACO folder has not been approved, ask whether to use an existing folder or create `ACO — Art & Commerce Office`. Never scan unrelated Drive content just to discover context.

## Recommended private structure

```text
ACO — Art & Commerce Office/
  Contexts/
  History/
  Projects/
  Clients/
  Handoffs/
  Archive/
```

Users may choose a different folder name or storage system. ACO should only use locations the user explicitly identifies or approves.

## Context loading

Load only what a task needs. Use BLIND-FIRST research or critique when existing context could bias the result.

Typical context files include:

- `artist-context.md`
- `company-context.md`
- `career-context.md`
- `job-search-context.md`
- `legal-context.md`
- project/client-specific context as needed

## History

Maintain continuity separately from canonical context:

- `WORK-LOG.md` — what was done
- `DECISIONS.md` — decisions actually confirmed
- `OPEN-LOOPS.md` — unresolved items
- `CONTEXT-CHANGELOG.md` — how canonical context changed
- `APPLICATIONS.md` — job-search pipeline
- `LEGAL-MATTERS.md` — legal matters/deadlines

## Privacy / least context

- Do not search an entire Drive when an approved ACO folder or explicit file can answer the task.
- Do not store credentials, passwords, access tokens, or unnecessary sensitive data in context.
- Do not copy private context into the public GitHub repository.
- Treat context as mutable and versioned; separate facts from hypotheses and preferences.

## ChatGPT / Codex Desktop to VS Code handoff

For coding or production work, export only the relevant subset of private knowledge into a temporary project-local folder:

```text
.agent-context/
  CURRENT-BRIEF.md
  RELEVANT-CONTEXT.md
  DECISIONS.md
  OPEN-LOOPS.md
  WORK-LOG.md
  CHANGES.md
  HANDOFF.md
```

At the end of substantial IDE work, record what changed, what was decided, what remains unresolved, tests performed, and the recommended next step. A later Context Steward pass should promote only durable changes back to the private knowledge store.

## Authority rule for artist practice

When multiple offices work together on an artist's own work:

- Artist Office owns artistic intent and final artistic decisions.
- Agency Office supports communication, experience, presentation and audience work.
- Product Office supports technical realization.
- Organization Office supports institutional/programmatic questions when relevant.

Technical or marketing convenience should not redefine the artwork by default.
