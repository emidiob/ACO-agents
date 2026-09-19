# Agency Office

A generic specialist module for a **creative production + brand strategy + design + marketing agency**.

The module contains **55 agency-specific agents**. It deliberately reuses organization-office and shared specialists where the expertise is the same rather than duplicating them.

## Operating model

```text
DIRECTORS
make consequential decisions
    ↓
SPECIALISTS
solve domain problems and define systems
    ↓
JUNIOR / MAKERS / COORDINATORS
research, generate, prototype, adapt, verify and execute
```

The orchestrator defaults to the lowest-seniority role capable of doing the task well. For substantial exploratory work, the preferred pattern is **junior/research first pass → specialist review → director decision**.

## One-line invocation

In a configured project, the user should be able to write:

> Use the Agency Office.

Then brief the job naturally. `agency_orchestrator` chooses context, team, sequence and escalation. The user does not need to name individual agents unless they want to.

## Agency-specific roles

### Orchestration
- `agency_orchestrator`

### Strategy
- `strategy_director`
- `research_insights_director`
- `cultural_strategist`
- `audience_strategist`
- `creative_strategist`
- `campaign_strategist`

### Brand + Design
- `design_director`
- `verbal_identity_director`
- `copywriter`
- `brand_identity_designer`
- `motion_design_director`
- `digital_design_director`
- `brand_guardian`

### Production
- `integrated_producer`
- `film_producer`
- `photography_producer`
- `postproduction_supervisor`
- `cgi_vfx_supervisor`
- `business_affairs_manager`

### Content + Marketing
- `content_director`
- `social_media_manager`
- `media_strategy_planner`
- `performance_marketing_manager`
- `crm_lifecycle_strategist`
- `creator_partnerships_manager`
- `organic_discovery_strategist`

### Delivery
- `project_manager`
- `traffic_resource_manager`

### Junior / Makers / Coordinators
- `junior_brand_strategist`
- `design_researcher`
- `junior_designer`
- `production_designer`
- `junior_art_director`
- `visual_researcher`
- `junior_copywriter`
- `copy_researcher`
- `social_content_creator`
- `community_manager`
- `content_researcher`
- `junior_media_planner`
- `marketing_analyst`
- `seo_content_researcher`
- `junior_producer`
- `production_coordinator`
- `postproduction_coordinator`
- `casting_researcher`
- `location_researcher`
- `creative_technologist_prototyper`
- `frontend_prototyper`
- `presentation_designer`
- `fact_checker`
- `project_coordinator`
- `traffic_coordinator`
- `asset_manager`

## Reused specialists

The installer also brings in relevant generic roles from `organization-office/` and all reusable roles from `shared/`, including `creative_director`, `account_director`, `client_strategy_director`, `business_development_director`, `executive_producer`, `creative_technologist`, `product_experience_director`, `ux_service_designer`, `contracts_ip_manager`, `data_insights_analyst`, `brand_strategist`, `art_director`, `marketing_strategist`, finance and editing roles.

## Context

Keep agency identity and client information outside the agent prompts. Typical context stack:

```text
company-context.md
+ client-context.md
+ brand-context.md
+ project-context.md
+ campaign-context.md
+ current brief
```

Use `NONE/BLIND`, `LIGHT`, `FULL` or `BLIND-FIRST` context modes as described in the repository `CONTEXT-POLICY.md`.
