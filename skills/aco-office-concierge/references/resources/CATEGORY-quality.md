# Quality resources

Optional catalogue, not an installation list. Consult current source and actual host capabilities.

## promptfoo

**Promptfoo** · tool · source_reviewed · reviewed 2026-09-20

Source: https://github.com/promptfoo/promptfoo

**Use:** Run authorized prompt/model regression or security evaluations with fixed inputs and budgets.

**Avoid:** Model calls can incur costs and disclose data. Red-team only owned or authorized targets. Scores need human interpretation.

**Checks:** Model calls can incur costs and disclose data. Red-team only owned or authorized targets. Scores need human interpretation.

Roles: `skill_evaluation_engineer`, `llm_engineer`, `security_reviewer`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/QUALITY-AND-EVALUATION.md). External upstream content is not bundled. No execution tests performed.

## gitleaks

**Gitleaks** · tool · source_reviewed · reviewed 2026-09-20

Source: https://github.com/gitleaks/gitleaks

**Use:** Run a real secret scan before a release when installed and permitted.

**Avoid:** An unrun or clean scan does not prove no secret exists. Redact findings; never print a detected credential in a public report.

**Checks:** An unrun or clean scan does not prove no secret exists. Redact findings; never print a detected credential in a public report.

Roles: `security_engineer`, `code_reviewer`, `release_manager`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/QUALITY-AND-EVALUATION.md). External upstream content is not bundled. No execution tests performed.

## semgrep

**Semgrep** · tool · source_reviewed · reviewed 2026-09-20

Source: https://github.com/semgrep/semgrep

**Use:** Apply reviewed static-analysis rules to authorized code and triage findings.

**Avoid:** Inspect exact rule licences and cloud behavior. Static analysis does not replace execution testing or expert security review.

**Checks:** Inspect exact rule licences and cloud behavior. Static analysis does not replace execution testing or expert security review.

Roles: `security_reviewer`, `code_reviewer`, `tech_lead`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/QUALITY-AND-EVALUATION.md). External upstream content is not bundled. No execution tests performed.
