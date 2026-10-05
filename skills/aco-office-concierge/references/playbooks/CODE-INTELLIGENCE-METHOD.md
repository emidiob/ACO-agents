# Code Intelligence Method

Use code-intelligence tools to reduce unnecessary repository loading, not to replace the repository as source of truth.

## Method
1. Lock the repository/worktree and current revision.
2. Read repository instructions and the files closest to the requested change.
3. If a verified local code-intelligence capability exists, query only the structural question needed: symbols, callers/callees, dependency path, route, impact surface or known architecture decision.
4. Verify consequential architecture/behavior claims against current source when the index may be stale or HEAD has changed.
5. Make the smallest coherent change and run relevant tests/checks.
6. Refresh/invalidate the local index when supported.
7. Persist only a materially useful human-readable architecture/decision summary in the existing canonical ACO document; never mirror ASTs, call graphs, embeddings or source files to Drive.

## Evidence
A code-intelligence answer is a retrieval accelerator, not proof that code compiles/runs. Record repository/revision provenance when a durable architecture note depends on it.

## Tool boundary
External code-memory/MCP tools are optional. Verify exact source/version/license, filesystem scope, network behavior and host authorization before use. ACO does not install or bundle them automatically.
