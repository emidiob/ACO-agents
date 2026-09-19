# Private Context MCP Roadmap

The public plugin is intentionally skills-only. A private MCP server can later provide persistence and controlled access to context/history.

## Suggested resources/tools

### Read
- `get_context(scope, depth)`
- `get_history(scope, since?)`
- `get_decisions(scope, status?)`
- `get_open_loops(scope)`
- `search_knowledge(query, scope?)`

### Write
- `append_work_log(scope, entry)`
- `record_decision(scope, entry)`
- `add_open_loop(scope, entry)`
- `close_open_loop(scope, id, resolution)`
- `propose_context_update(scope, patch)`
- `approve_context_update(scope, proposal_id)`

## Safety / governance

- Require explicit approval before changing canonical context when a change is strategic, identity-defining, legally sensitive, or not directly evidenced.
- Keep history append-only.
- Mark superseded decisions rather than deleting them.
- Avoid storing credentials/secrets.
- Keep artist/company/career/legal scopes separated.
- Use least-privilege authentication and per-scope permissions.
