# Development resources

Optional catalogue, not an installation list. Consult current source and actual host capabilities.

## javascript-algorithms

**JavaScript Algorithms and Data Structures** · reference · source_reviewed · reviewed 2026-09-20

Source: https://github.com/trekhleb/javascript-algorithms

**Use:** Study or compare classic algorithms/data structures when a real implementation decision benefits from them.

**Avoid:** Do not cargo-cult example code into production; choose the simplest appropriate standard-library/data-structure solution and verify complexity/tests.

**Checks:** Reference repository, not a runtime dependency. Check current examples and language/runtime constraints before adapting anything.

Roles: `junior_developer`, `frontend_engineer`, `code_reviewer`.

Required capabilities when executing: none declared; inspect the actual task/tool.

[Original ACO method](../playbooks/CODE-REFERENCE-METHOD.md). External upstream content is not bundled. No execution tests performed.

## thirty-seconds-code

**30 Seconds of Code** · reference · source_reviewed · reviewed 2026-09-20

Source: https://github.com/30-seconds/30-seconds-of-code

**Use:** Use short examples as a discovery/learning aid for common JavaScript and web tasks.

**Avoid:** Do not paste snippets blindly, treat brevity as correctness, or use a snippet instead of a maintained dependency/API when that is safer.

**Checks:** Educational/reference material only; production code still needs stack-specific review, tests and security checks.

Roles: `junior_developer`, `frontend_engineer`, `technical_writer`.

Required capabilities when executing: none declared; inspect the actual task/tool.

[Original ACO method](../playbooks/CODE-REFERENCE-METHOD.md). External upstream content is not bundled. No execution tests performed.

## public-apis

**Public APIs** · catalogue · source_reviewed · reviewed 2026-09-20

Source: https://github.com/public-apis/public-apis

**Use:** Discover candidate public APIs for prototypes or integrations before verifying the provider directly.

**Avoid:** A catalogue entry is not proof the API is free, active, lawful for the use case, secure, stable or suitable for production.

**Checks:** Verify official provider docs, authentication, quotas, terms, data rights, geographic restrictions and current status before implementation.

Roles: `api_researcher`, `api_integration_engineer`, `product_researcher`.

Required capabilities when executing: none declared; inspect the actual task/tool.

[Original ACO method](../playbooks/CODE-REFERENCE-METHOD.md). External upstream content is not bundled. No execution tests performed.

## openhands

**OpenHands** · runtime · source_reviewed · reviewed 2026-09-20

Source: https://github.com/All-Hands-AI/OpenHands

**Use:** Use as an optional autonomous coding runtime for a bounded repository task when sandbox, branch, tests and review are configured.

**Avoid:** Do not hand it unrestricted credentials/repos, confuse cloud/enterprise/core licensing, or accept changes without diff/tests/human review.

**Checks:** External coding-agent runtime. Core is MIT according to current project docs; enterprise features have separate terms. ACO itself already has Codex workflows, so use only when it adds real value.

Roles: `software_architect`, `tech_lead`, `code_reviewer`, `product_software_orchestrator`.

Required capabilities when executing: local_execution_or_external_service.

[Original ACO method](../playbooks/SOFTWARE-AGENT-EXECUTION.md). External upstream content is not bundled. No execution tests performed.
