# ACO — complete command menu

Claude Code uses `/name`; Codex uses `$name`. Availability requires host discovery.

Use `/aco webdesign`, `/aco motion`, `/aco video`, `/aco image`, `/aco capture`, `/aco genjutsu`, `/aco skills` or `/aco help` as Concierge routes. In Codex pass these arguments to `$aco`.

## Creative shortcuts and help

| Claude Code | Codex | Purpose |
|---|---|---|
| `/aco` | `$aco` | ACO Concierge entrypoint. Invoke as /aco in Claude Code or $aco in Codex. Route creative, studio and organizational tasks using the canonical ACO runtime. |
| `/aco-capture` | `$aco-capture` | ACO Capture photographic prompting with Frame → Moment → Light → Matter, seven capture methods and realistic camera setups. |
| `/aco-genjutsu` | `$aco-genjutsu` | Analyze a supplied video and prepare reference-guided recreation, motion-transfer or selective-edit prompts. Creates visual reference files before drafting timed prompts; video rendering remains a separate action. |
| `/aco-help` | `$aco-help` | Show all ACO commands: creative shortcuts, offices, context tools and terminal/runtime discovery, with Claude Code and Codex syntax. |
| `/aco-image` | `$aco-image` | Photographic and generative-image prompts using ACO methods, including Nano Banana and Seedream candidate adapters. |
| `/aco-motion` | `$aco-motion` | Native ACO motion design: create, animate, preview and export video graphics; captions, maps, editable timelines and video apps; build and audit CSS/Motion/GSAP UI animation. |
| `/aco-skills` | `$aco-skills` | Display ACO technical skills and clear experimental status; /aco-skills lists the whole registry without running models. |
| `/aco-video` | `$aco-video` | AI video direction and provider-aware prompting, including Seedance candidate techniques, storyboard, camera, timing and QC. |
| `/aco-webdesign` | `$aco-webdesign` | Design, build and redesign websites and product interfaces with original ACO art direction, searchable design recipes, reusable tokens, functional states and browser verification. |

## Offices

| Claude Code | Codex | Purpose |
|---|---|---|
| `/aco-administration-office` | `$aco-administration-office` | Administration & Secretariat: Inbox, appointments, meetings, files, travel, email, WhatsApp and call preparation or authorized tool execution. |
| `/aco-agency-office` | `$aco-agency-office` | Brand strategy, creative direction, design, production, marketing and client delivery. |
| `/aco-artist-office` | `$aco-artist-office` | Develop, critique, plan, produce, document and sustain an artistic practice. |
| `/aco-commercial-office` | `$aco-commercial-office` | Commercial & Sales: Offers, sales pipelines, qualifying leads, pitches, tenders and client retention; art sales remain led by Artist Office. |
| `/aco-delivery-office` | `$aco-delivery-office` | Project & Programme Delivery: Cross-project plans, dependencies, resourcing, change control and acceptance; reuse existing project managers, do not duplicate them. |
| `/aco-finance-office` | `$aco-finance-office` | Finance & Business Control: Project economics, budgets, cash flow, billing, bookkeeping coordination and royalties; not banking execution or certified tax advice. |
| `/aco-legal-office` | `$aco-legal-office` | First-pass jurisdiction-aware legal research, contract review, rights and matter organization. |
| `/aco-office-concierge` | `$aco-office-concierge` | Front door: resolve the request, minimal team, scope and context; coordinate work and verified continuity. |
| `/aco-organization-office` | `$aco-organization-office` | Research-led organizational strategy, culture, programmes, publishing, partnerships and operations. |
| `/aco-people-office` | `$aco-people-office` | People & HR: Employer-side workforce planning, job briefs, recruitment coordination, onboarding and people operations; candidate job search stays with Recruitment Office. |
| `/aco-product-office` | `$aco-product-office` | Websites, applications, software, AI features, UX, engineering, tests and release preparation. |
| `/aco-production-office` | `$aco-production-office` | Production & Postproduction: Film, photography, CGI, editing, grading, retouching, sound, generative media and ComfyUI. Operate real software only through available authorized tools. |
| `/aco-publishing-office` | `$aco-publishing-office` | Publishing & Media: Books, catalogues, magazines, digital publications, newsrooms, newsletters, podcasts, rights, distribution, subscriptions and advertising. |
| `/aco-recruitment-office` | `$aco-recruitment-office` | Candidate-side job discovery, career strategy, CV, portfolio, applications, interviews and offer preparation. |

## Context

| Claude Code | Codex | Purpose |
|---|---|---|
| `/aco-context-setup` | `$aco-context-setup` | Initialize or extend private ACO knowledge safely; multiple organizations, activities, clients, brands and projects. |
| `/aco-context-steward` | `$aco-context-steward` | Maintain auditable session events, approved decisions, open loops, context proposals and verified handoffs. |

## Internal methods and terminal tools

Role IDs such as `motion_designer` are internal methods, not native commands. Use the office role index when you need them.
`aco-skills` shows the separate technical registry and its active/candidate status. Native entry skills and external upstream skills are not additional validated registry entries.
From a complete source checkout: `python3 scripts/aco_cli.py --help` lists every actual terminal subcommand. In an installed root use `aco-office-concierge/runtime/scripts/aco_cli.py --help`.
Common terminal tools include `install`, `install-status`, `validate`, `skill-search`, `skill-resolve`, `capability-audit`, `goal-status` and `autonomy-plan`. Inspect `<command> --help` for arguments; these are not slash commands.

## Native motion design

`aco-motion` contains native ACO methods for create, animate, captions, maps, edit, preview, render, app, web, audit and upgrade. These are arguments to the skill, not additional registered commands. No external agent skill is required; real engines and project dependencies are checked per task.

## Native web design

`aco-webdesign <operation> <target>` selects an ACO method. In Codex use `$aco-webdesign`; in Claude use `/aco-webdesign`. These arguments are not separate host commands.

`init`, `document`, `extract`, `shape`, `craft`, `critique`, `audit`, `polish`, `bolder`, `quieter`, `distill`, `harden`, `onboard`, `animate`, `colorize`, `typeset`, `layout`, `delight`, `overdrive`, `clarify`, `adapt`, `optimize`, `live`, `generate`, `motion-review`, `motion-opportunities`, `motion-performance`, `motion-vocabulary`, `mobile-native`, `break-ui`, `prototype`, `react-review`, `libraries`.

The native kit also provides external-data search, design-system proposals and a rendered-DOM audit.
