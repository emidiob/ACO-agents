# Execution workflow state

ACO may represent substantial work as a compact state sequence without creating a new project file. State can live in chat, a task runtime, a worktree handoff or the existing canonical/pipeline record when durable.

Supported lifecycle states are:

```text
proposed → prepared → approved? → executing → executed → checked → reviewed? → closed
                                      ↘ unknown → reconciled ↗
                                      ↘ failed / blocked
```

Approval is required only when the actual action level requires it; do not add ceremony to safe reversible work. `executed`, `checked`, `reviewed` and `closed` require evidence appropriate to the claim. An `unknown` execution result blocks normal progression until reconciled.

Workflow state is **not** permission, a project-creation trigger or a reason to create a permanent log file. Follow Compact Memory and Pipeline ≠ Project.
