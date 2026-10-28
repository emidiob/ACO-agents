# ACO Webdesign — feature parity status

This is an implementation audit, not a completed parity claim. The user selected independent ACO engines/methods with external datasets allowed. Revisions are pinned; upstream additions require a new audit. The inventory still needs component-level expansion for React Bits and shadcn and rule-level expansion for Impeccable. Full parity is **not achieved**.

## [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/28b3b8dee8c976df4fa3e94aed4e092ad43fcb03)

| Capability | State | Outstanding work |
|---|---|---|
| Search all supplied design domains | partial | Independent BM25 works; upstream relevance and aliases are not equivalent. |
| Search stack-specific guidance | implemented | Search provided stacks/<name> CSV; local execution verified on React. |
| Generate a coordinated design system | partial | Evidence-linked selections and CSS colors; conditional reasoning and all design dials remain missing. |
| Persist master and page overrides | partial | New-directory persistence and color overrides; no master/page merge engine. |
| Refresh external catalogs with provenance | partial | Pinned checksum fetch; no discovery/update or font catalog refresh engine. |

## [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill/tree/12af471f627f866411b4bd785b19646d3672784c)

| Capability | State | Outstanding work |
|---|---|---|
| Seeded directions, keep/redraw/alternatives | missing | Six original recipes do not cover upstream direction selection. |
| App styles, shells and screen patterns | partial | Working example; no app direction engine. |
| Open-archive search and attribution | missing | No native archive discovery or attribution exporter yet. |
| Scroll scenes and motion implementations | missing | ACO Motion guidance does not implement this scene catalog. |
| Browser geometry and house-rule inspection | partial | 17 original checks; no upstream rule equivalence or automated screenshot capture. |
| Three-width screenshot review and repair | partial | Two widths tested previously; no equivalent automatic inspection engine. |
| Working charts with consistent data | missing | Example workspace does not provide chart rendering library. |

## [pbakaus/impeccable](https://github.com/pbakaus/impeccable/tree/7510e233b228864606888d252abacf5e7148bf87)

| Capability | State | Outstanding work |
|---|---|---|
| 24 scoped design operations | partial | Original methods are written; no behavioral parity tests for each operation. |
| 62 deterministic frontend detectors | missing | The new 17-check DOM audit is a different, smaller rule set. |
| Live browser selection and source-linked editing | missing | Manual live method is not a live bridge. |
| Automatic element variants and comparison | partial | Method only; no automated variant engine. |
| Separate product facts and implemented design | partial | Methods only; no context discovery engine. |
| Host edit hooks and trusted installation | missing | No native edit-hook implementation. |
| Browser extension | missing | No extension implemented. |
| Font catalog and inspection | partial | External font metadata searchable; no font preview/inspection subsystem. |
| Shortcut pinning and runtime diagnostics | missing | Operation lookup is not native shortcut installation or engine diagnostics. |

## [anthropics/skills](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44)

| Capability | State | Outstanding work |
|---|---|---|
| Brief-specific frontend design | partial | Original method; no matched-brief output comparison. |
| React artifact scaffold and single HTML bundle | missing | Existing scaffold is static HTML only. |
| Server lifecycle and browser test harness | partial | Manual host browser checks; no independent test harness. |

## [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62)

| Capability | State | Outstanding work |
|---|---|---|
| Source-based interface audit | partial | Selected original checks; no exhaustive rule coverage. |
| React performance review | partial | Method and external searchable dataset; not verified against full upstream rule corpus. |
| React composition patterns | partial | General method; no dedicated pattern coverage tests. |
| React view transitions | missing | No native version-aware transition adapter. |
| Interface writing review | partial | Method present; no comparative evaluation. |
| Measured web optimization | partial | Method present; profiler integration unimplemented. |

## [emilkowalski/skills](https://github.com/emilkowalski/skills/tree/2d228630ba1446365f614a108cb8252f1feda202)

| Capability | State | Outstanding work |
|---|---|---|
| Create, review, improve and discover motion | partial | Original methods; not behaviorally compared on shared fixtures. |
| Diagnose dropped frames | partial | Method only; no profiler collector. |
| Functional alternatives with switcher | partial | Method only; no switcher generator. |
| Mobile web behavior | partial | Method only; real device checks outstanding. |
| Worst-case content testing | partial | Method only; fixture generator outstanding. |
| Sonner integration and troubleshooting | missing | No native Sonner adapter or test project. |
| Apple interaction principles applied to web | missing | No dedicated native method or benchmark. |

## [DavidHDev/react-bits](https://github.com/DavidHDev/react-bits/tree/e12c22192ac7b4b452c5e2feb9b586d74765d696)

| Capability | State | Outstanding work |
|---|---|---|
| Animated text, components, backgrounds and interactions | missing | Requires original implementations and a component-by-component inventory. |
| JavaScript/TypeScript and CSS/Tailwind variants | missing | No equivalent native catalog. |
| Background, texture, shape, stage and sound tools | missing | No original tools implemented; upstream restricted source is not bundled. |

## [shadcn-ui/ui](https://github.com/shadcn-ui/ui/tree/96da9cc7f1aa10580a3741664e2a77c721206c00)

| Capability | State | Outstanding work |
|---|---|---|
| Complete component catalog and behavioral states | missing | No native component catalog; optional upstream use is not parity. |
| Registry search, install and dependency resolution | missing | No independent registry client. |
| Presets, theming and project setup | missing | CSS color export is not a preset engine. |
| Composable blocks and charts | missing | No complete native equivalents. |
| Radix/Base migration and debugging | missing | No independently implemented migration tooling. |

## Acceptance

Each feature needs an original implementation, realistic positive and negative fixtures, and actual execution evidence in supported hosts/stacks. Similar command names and documentation alone do not establish parity. Runtime visual capabilities need rendered comparisons; component parity includes behavior, keyboard interaction, responsive states, and supported variants. External datasets retain their licenses and source hashes. No full-parity release should be published while the inventory or required features remain incomplete.

## Component inventory

The pinned source trees identify 218 component families in DavidHDev/react-bits, 64 component families in shadcn-ui/ui. Names and source variant paths are recorded in `skills/aco-webdesign/references/component-inventory.json`. This metadata inventory is not copied component code or implementation evidence. Props, effects, blocks, tools and behavior still need individual acceptance tests.
