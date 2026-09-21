# Office resources

Optional catalogue, not an installation list. Consult current source and actual host capabilities.

## agentic-inbox

**Agentic Inbox** · integration · source_reviewed · reviewed 2026-09-20

Source: https://github.com/cloudflare/agentic-inbox

**Use:** Evaluate an optional dedicated agent mailbox deployment when existing authorized email tools do not fit.

**Avoid:** Do not replace Gmail by default or assume separate mailbox storage provides per-mailbox authorization.

**Checks:** README warns shared Access policy permits all mailbox access. Domain/routing/storage/cost and real access isolation must be reviewed.

Roles: `communications_operator`, `inbox_correspondence_manager`, `security_reviewer`.

Required capabilities when executing: server_deployment, mailbox_account.

[Original ACO method](../playbooks/OFFICE-RECIPES.md). External upstream content is not bundled. No execution tests performed.

## twenty

**Twenty CRM** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/twentyhq/twenty

**Use:** Use an existing authorized CRM when relationship scale exceeds compact inline records.

**Avoid:** No CRM migration or email/calendar sync by default. An art relationship is not just a sales stage; preserve confidentiality and opt-in rules.

**Checks:** No CRM migration or email/calendar sync by default. An art relationship is not just a sales stage; preserve confidentiality and opt-in rules.

Roles: `sales_operations_manager`, `collector_relations_manager`, `institutional_relations_manager`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/VERIFIED-TOOLING.md). External upstream content is not bundled. No execution tests performed.

## plane

**Plane** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/makeplane/plane

**Use:** Coordinate an existing team’s issues and delivery through a verified integration.

**Avoid:** No duplicate tracking system if compact plans suffice. A listed MCP feature is not a connected or authorized tool.

**Checks:** No duplicate tracking system if compact plans suffice. A listed MCP feature is not a connected or authorized tool.

Roles: `project_manager`, `programme_delivery_manager`, `delivery_orchestrator`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/VERIFIED-TOOLING.md). External upstream content is not bundled. No execution tests performed.

## n8n

**n8n** · runtime · source_reviewed · reviewed 2026-09-20

Source: https://github.com/n8n-io/n8n

**Use:** Implement explicitly approved recurring workflows with an actual scheduler and receipts.

**Avoid:** Source-available/fair-code terms need separate review; do not imply unrestricted redistribution. Approve credentials, targets, cost, timezone and stop behavior.

**Checks:** Source-available/fair-code terms need separate review; do not imply unrestricted redistribution. Approve credentials, targets, cost, timezone and stop behavior.

Roles: `api_integration_engineer`, `administration_orchestrator`, `communications_operator`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/VERIFIED-TOOLING.md). External upstream content is not bundled. No execution tests performed.
