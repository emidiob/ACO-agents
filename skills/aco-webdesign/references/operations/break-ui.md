# Stress-test interface content

Use controlled fixtures for zero/many records, very long unbroken strings, emoji, RTL, large counts, missing media and asynchronous failures. Apply them through project data/test seams, not production data mutations.

Completion evidence: Failures reproduce with fixtures and fixes preserve ordinary content behavior.

Use the project’s existing conventions and available tools. Report missing capabilities explicitly; a written procedure is not runtime proof.

Generate synthetic stress content with `scripts/prototype_review.py stress --seed 42`. Bind each relevant case to the actual component props or a test route and inspect the result; generating fixture JSON alone is not a test pass. See [project tools](../project-tools.md).
