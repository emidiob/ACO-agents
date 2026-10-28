# Implement the requested interface

Inspect framework, package versions, routing, styles, tests and data flow first. Reuse established components. For a new small static site semantic HTML/CSS and a little JavaScript may be sufficient; a product application may need the existing framework and data architecture. Verify unfamiliar library APIs from official docs rather than inventing imports.

Build the core task and layout with realistic-length content. Use actual navigation targets; a primary button must perform its named action. Clearly label a local prototype that has no backend. Do not imply email delivery, persistence, authentication or payment from a UI-only interaction.

Use native controls where possible. Make state changes readable and announce material asynchronous results. Keep focus visible, preserve keyboard order, return focus after closing a dialog and provide alternatives to pointer-only gestures. Allow text zoom and long labels. At narrow widths recompose priority and navigation; do not simply shrink the desktop layout or conceal overflow with a blanket clip.

Reserve media dimensions and load only what the page needs. Verify image source/license and alt behavior. Do not ship external images or install dependencies merely because a reference demo uses them. Add animation to clarify a transition or action, with reduced-motion behavior and interruption handling. For complex motion use the existing project engine or optional ACO Motion; do not introduce a new animation dependency for a trivial fade.

Run the project checks, then inspect the rendered page and exercise the key flow. Document unfinished production connections explicitly. A user request to build authorizes the local implementation, not an unrequested public deployment.
