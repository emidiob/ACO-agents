# Evidence-led website acceptance

## Contract before tests
List the critical routes, user tasks, content states and acceptance IDs. Separate visual judgement, functional behaviour, accessibility, performance and security. A single score cannot represent all five.

## Verification loop
1. Run the actual application with the project's existing scripts in an authorized environment. Read failures; do not replace the project stack merely because a preferred starter works.
2. Establish deterministic test conditions: build/commit, browser, OS, viewport, data fixture, locale, motion setting and font readiness. Avoid real client data in public screenshots or CI fixtures.
3. Capture representative initial and interaction states. With an available browser/test runner, test navigation, forms, dialogs, empty/error states, long content, zoom and reduced motion. Do not simulate an observed screenshot in prose.
4. Walk the critical flow by keyboard. Check visible focus, meaningful order, focus restoration after dialogs, error association and announcements. Use actual assistive-technology checks where available; do not claim a screen-reader test based on an HTML scan.
5. Compare like-for-like screenshots with the approved reference. Use masks only for documented nondeterministic areas, never to hide defects. Review any baseline update independently.
6. Measure performance under stated conditions. Address user-visible request waterfalls, oversized media/bundles and expensive rendering before micro-optimizing. Synthetic measurement is not real-user performance evidence.
7. Re-test the changed behaviour and nearby regressions. Preserve failing evidence. Do not reduce thresholds until a broken test becomes green.
8. Report acceptance by ID: passed, failed, planned or not_run; attach reproduction steps and actual evidence paths. ACO's evidence checker verifies file integrity and coverage, not the truth of every statement inside a report.

## Additional primary references
- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)
- [WCAG contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

## Definition of done
The user can complete the intended task; known blockers are fixed or explicitly accepted; visual review and tests are documented. If tools are missing, deliver the implementation and a precise remaining test list. Never equate static checks with a production signoff.

## Research provenance and limits

Comparison references: [S01](https://github.com/anthropics/skills), [S06](https://github.com/github/awesome-copilot), [S09](https://github.com/pbakaus/impeccable), [S11](https://github.com/vercel-labs/agent-skills).
This is an ACO-authored operating procedure, not a bundled upstream skill. No external installer, runtime, prompt collection, palette/font dataset or model weights are included. Read the source inventory for inspection scope and licence cautions. Source popularity is not a quality benchmark.
