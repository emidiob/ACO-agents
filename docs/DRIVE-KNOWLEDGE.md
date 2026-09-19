# Google Drive as the private knowledge layer

ACO — Art & Commerce Office keeps reusable agent logic public and private knowledge outside the repository.

## Recommended architecture

```text
GitHub repository
  plugin + skills + generic agents + templates
          |
          v
Google Drive — private source of truth
  ACO — Art & Commerce Office/
    Contexts/
    History/
    Projects/
    Clients/
    Handoffs/
    Archive/
```

The public repository should never contain filled artist, company, career, client, legal, or project context.

## Context loading

Load only what a task needs. Use blind-first research or critique when existing context could bias the result.

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

## ChatGPT / Codex Desktop to VS Code handoff

For a coding or production task, export only the relevant subset of private knowledge into a temporary local folder:

```text
.agent-context/
  CURRENT-BRIEF.md
  RELEVANT-CONTEXT.md
  DECISIONS.md
  OPEN-LOOPS.md
  HANDOFF.md
```

The IDE session should update its local work log and handoff. A later Context Steward pass promotes only durable changes back into Google Drive.

## Authority rule for artist practice

When multiple offices work together on an artist's own work:

- Artist Office owns artistic intent and final artistic decisions.
- Agency Office supports communication, experience, presentation and audience work.
- Product Office supports technical realization.
- Organization Office supports institutional/programmatic questions when relevant.

Technical or marketing convenience should not redefine the artwork by default.
