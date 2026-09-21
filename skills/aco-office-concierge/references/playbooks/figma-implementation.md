# Figma-to-code reconciliation

## Preconditions
A real file/node reference or supplied design artefact, authorized design access, repository access and target stack. If the reference is absent or cannot be read, stop guessing at pixel-perfect fidelity and ask for the target.

## Procedure
1. Resolve exact page/node/component versions. Read design context and a visual reference; record which design revision was used. Do not infer inaccessible pages or hidden variants.
2. Inventory existing code components, tokens, assets and naming before generating new ones. Map design components to actual code equivalents where evidence exists.
3. Separate values explicitly specified in the design from responsive behaviour that must be inferred. Clarify consequential gaps: interaction, content, breakpoints and accessibility, not every spacing detail.
4. Use provided export assets with appropriate rights. Never replace meaningful imagery with arbitrary placeholders and call the result faithful. Mark missing assets explicitly.
5. Implement one representative section and state, then inspect it in the browser at the design frame dimensions. Fix structural mismatches before polishing shadows or offsets.
6. Add responsive and keyboard behaviour in a way that preserves hierarchy. A screenshot is not a specification for semantics, error recovery or narrow-screen behaviour.
7. Compare screenshot evidence at the same viewport, font readiness and content. Record intentional deviations and their approval, rather than changing golden baselines to make tests pass.
8. Deliver working components, node-to-component map, remaining deviations and tests. Do not claim a live Figma edit, Code Connect binding or deployment without the exact tool receipt.

## Boundary
A Figma MCP capability may be available separately; ACO does not install or authorize it. Reading a design, modifying a design and publishing a site are separate permissions.

## Research provenance and limits

Comparison references: [S15](https://github.com/openai/plugins), [S05](https://github.com/VoltAgent/awesome-claude-code-subagents), [S06](https://github.com/github/awesome-copilot).
This is an ACO-authored operating procedure, not a bundled upstream skill. No external installer, runtime, prompt collection, palette/font dataset or model weights are included. Read the source inventory for inspection scope and licence cautions. Source popularity is not a quality benchmark.
