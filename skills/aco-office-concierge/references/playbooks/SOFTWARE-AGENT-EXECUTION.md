# External software-agent execution

Use autonomous coding runtimes only for bounded work with reviewable evidence.

- Give the agent a precise repository/task scope, branch and acceptance tests.
- Use a sandbox/worktree and least-privilege credentials.
- Preserve unrelated work and prohibit destructive commands/force push unless separately authorized.
- Require command/test outputs, diff review and human approval before merge/deploy.
- Treat cloud integrations and enterprise features as separate permission/license surfaces.
- ACO records durable decisions and handoff, not the agent’s private chain-of-thought.
