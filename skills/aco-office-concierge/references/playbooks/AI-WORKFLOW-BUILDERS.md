# AI workflow builders

For visual/managed agent, RAG and automation platforms.

1. First decide whether a platform is needed; simple code/native host tools may be easier to maintain.
2. Define inputs, outputs, data boundaries, model/provider, retrieval source, failure path and human approval points before drawing the flow.
3. Keep secrets in an approved secret store, never in exported flows or ACO memory.
4. Version prompts/config, test with representative cases and record model/provider versions.
5. Separate prototype convenience from production requirements: auth, RBAC, logs, backups, observability, cost and vendor/license terms.
6. Export only the durable architecture/decisions to ACO, not every platform-internal node/state.
