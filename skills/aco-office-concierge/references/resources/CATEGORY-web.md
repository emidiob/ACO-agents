# Web resources

Optional catalogue, not an installation list. Consult current source and actual host capabilities.

## dotmatrix

**Dot Matrix loaders** · component · source_reviewed · reviewed 2026-09-20

Source: https://dotmatrix.zzzzshawn.cloud/

**Use:** React loading-state components; use only when actual waiting needs feedback.

**Avoid:** Do not add artificial waiting, mandatory loaders or decorative motion to every view.

**Checks:** Check per-component source/license, shadcn registry contents and framework compatibility before copying.

Roles: `frontend_engineer`, `interaction_designer`.

Required capabilities when executing: local_package_review.

[Original ACO method](../playbooks/MOTION-INTEGRATION.md). External upstream content is not bundled. No execution tests performed.

## playwright-cli

**Playwright CLI** · browser_tool · source_reviewed · reviewed 2026-09-20

Source: https://github.com/microsoft/playwright-cli

**Use:** Inspect an authorized running website, interactions, screenshots and browser errors.

**Avoid:** CLI, library and MCP are different entry points. Do not disable sandbox/security or assume browser execution from static code.

**Checks:** Inspect installed version/help, browser binary and current upstream instructions. No automatic installs.

Roles: `qa_engineer`, `test_automation_engineer`, `visual_design_critic`.

Required capabilities when executing: browser_execution.

[Original ACO method](../playbooks/MOTION-INTEGRATION.md). External upstream content is not bundled. No execution tests performed.

## react-three-fiber

**React Three Fiber** · library · source_reviewed · reviewed 2026-09-20

Source: https://github.com/pmndrs/react-three-fiber

**Use:** Build intentional interactive 3D in React with controlled scene lifecycle.

**Avoid:** Do not convert ordinary editorial sites to 3D unnecessarily or run multiple unmanaged render loops.

**Checks:** Check React/R3F/Three peer versions, device resources, texture/model licenses and renderer cleanup.

Roles: `creative_frontend_engineer`, `three_d_generalist`, `performance_engineer`.

Required capabilities when executing: local_package_review, webgl.

[Original ACO method](../playbooks/MOTION-INTEGRATION.md). External upstream content is not bundled. No execution tests performed.

## react-bits

**React Bits** · component · source_reviewed · reviewed 2026-09-20

Source: https://github.com/DavidHDev/react-bits

**Use:** Select a specific component pattern suited to the brief; integrate into the existing system.

**Avoid:** Do not assemble all demos into one site or treat gallery quantity as quality.

**Checks:** Inspect exact component dependencies, license/attribution and animation cost; do not assume blanket MIT.

Roles: `creative_frontend_engineer`, `frontend_prototyper`.

Required capabilities when executing: local_package_review.

[Original ACO method](../playbooks/MOTION-INTEGRATION.md). External upstream content is not bundled. No execution tests performed.

## open-seo

**OpenSEO** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/every-app/open-seo

**Use:** Run structured keyword, rank, competitor, backlink or site-audit work when live SEO data is actually needed.

**Avoid:** Do not infer SEO performance from generic advice or install a stack for a one-off question; external data-provider keys/costs and MCP permissions need separate review.

**Checks:** Repository documents MCP/agent-skill use and DataForSEO-backed workflows. Use current provider data and evidence, not cached claims.

Roles: `seo_content_researcher`, `marketing_strategist`, `data_insights_analyst`.

Required capabilities when executing: external_data_provider_or_self_host.

[Original ACO method](../playbooks/SEO-OPERATIONS.md). External upstream content is not bundled. No execution tests performed.

## radix-primitives

**Radix Primitives** · library · source_reviewed · reviewed 2026-09-20

Source: https://github.com/radix-ui/primitives

**Use:** Use suitable accessible interaction foundations for a custom React design.

**Avoid:** Library primitives do not certify the assembled interface. Test semantics, focus, keyboard, content, styling and real assistive behavior.

**Checks:** Library primitives do not certify the assembled interface. Test semantics, focus, keyboard, content, styling and real assistive behavior.

Roles: `frontend_engineer`, `design_system_designer`, `accessibility_specialist`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/DESIGN-TO-WEB.md). External upstream content is not bundled. No execution tests performed.

## storybook

**Storybook** · tool · source_reviewed · reviewed 2026-09-20

Source: https://github.com/storybookjs/storybook

**Use:** Isolate component states and review a reusable interface system.

**Avoid:** Useful for reusable systems; avoid unnecessary infrastructure for a tiny static page. Stories and snapshots are not comprehensive user testing.

**Checks:** Useful for reusable systems; avoid unnecessary infrastructure for a tiny static page. Stories and snapshots are not comprehensive user testing.

Roles: `design_system_designer`, `frontend_engineer`, `qa_engineer`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/DESIGN-TO-WEB.md). External upstream content is not bundled. No execution tests performed.

## lighthouse

**Lighthouse** · tool · source_reviewed · reviewed 2026-09-20

Source: https://github.com/GoogleChrome/lighthouse

**Use:** Collect repeatable lab diagnostics with the actual URL and configuration recorded.

**Avoid:** A score is not brand quality, full accessibility or real-user performance. Compare runs under matching conditions.

**Checks:** A score is not brand quality, full accessibility or real-user performance. Compare runs under matching conditions.

Roles: `performance_engineer`, `qa_engineer`, `frontend_engineer`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/DESIGN-TO-WEB.md). External upstream content is not bundled. No execution tests performed.

## axe-core

**axe-core** · library · source_reviewed · reviewed 2026-09-20

Source: https://github.com/dequelabs/axe-core

**Use:** Find detectable accessibility issues as one part of a manual and automated audit.

**Avoid:** No automated scan alone proves WCAG conformance; report checks not covered and manual findings.

**Checks:** No automated scan alone proves WCAG conformance; report checks not covered and manual findings.

Roles: `accessibility_tester`, `accessibility_specialist`, `qa_engineer`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/DESIGN-TO-WEB.md). External upstream content is not bundled. No execution tests performed.
