# Edit and compare a rendered change

For a trusted static HTML project, use the source-backed editor described in [interactive tools](../interactive-tools.md). Select the actual element, save text or supported inline style, and verify both the rendered result and source. Use undo/redo for reversible comparisons. A stale-source conflict must be resolved by reloading, not overwriting another change.

For Vite application components, use [framework tools](../framework-tools.md) to bind static JSX/TSX/Vue elements to the source editor. Use the project’s source editor for dynamic expressions and shared styles. Compare variants using identical content and viewport. Keep the selected implementation in source and verify relevant behavior after the change.

Completion evidence: the selected change is saved in the correct source file and visibly rendered. Report any unsupported source format or unavailable preview.
