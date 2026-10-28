# ACO — dependencies, API lookup and upgrades

Inspect the project manifest, lockfile, workspace layout and installed versions before coding. Prefer the project's existing package manager and local executable. Do not run a package installer just to look up documentation. For Remotion consult https://www.remotion.dev/docs/ and the relevant page's Markdown form when available; for Motion consult https://motion.dev/docs/; for GSAP use https://gsap.com/docs/v3/; for browser media consult https://mediabunny.dev/. Read exact API contracts from official docs or installed types. External agent-skill files are not required.

Before a package change identify the concrete missing capability. Match APIs to the installed version rather than silently upgrading to the latest docs. Read release notes for breaking changes and preserve user modifications. For Remotion keep core and related @remotion packages aligned to a compatible release; verify auxiliary package peer requirements separately instead of forcing every dependency to the same version.

When an upgrade is requested, record the current manifest/lockfile, choose an explicit compatible target, update only relevant dependencies and review the diff. Avoid upgrade commands that also install or rewrite external agent skills; use package-manager updates when necessary to preserve native ACO instructions. Validate types/build, representative frames, Studio editing if used and a short export when rendering changed.

For migration from legacy Framer Motion inspect actual import sites and breaking changes. Replace imports and dependencies coherently, keeping an existing working project intact until compatibility is confirmed. Do not mix version-specific examples and call the result verified.

Licenses for engines, fonts, footage, tiles and plugins remain separate from ACO instruction authorship. Use actual project requirements and current terms. Do not provision accounts, MCP servers, paid assets or cloud services as an automatic side effect of installing this skill.
