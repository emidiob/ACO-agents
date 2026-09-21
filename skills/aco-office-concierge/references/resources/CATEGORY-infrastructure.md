# Infrastructure resources

Optional catalogue, not an installation list. Consult current source and actual host capabilities.

## uptime-kuma

**Uptime Kuma** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/louislam/uptime-kuma

**Use:** Monitor uptime/endpoint availability for deployed websites, services and APIs after an explicit monitoring scope is approved.

**Avoid:** Availability is not full application health, security or UX quality; do not create recurring monitoring without a real deployment and alert destination.

**Checks:** External monitoring service. Document monitor ownership, interval, alert route and maintenance windows; ACO does not become an always-on monitor by referencing it.

Roles: `sre_engineer`, `devops_engineer`, `release_manager`.

Required capabilities when executing: server_deployment.

[Original ACO method](../playbooks/MONITORING-WATCHES.md). External upstream content is not bundled. No execution tests performed.

## vaultwarden

**Vaultwarden** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/dani-garcia/vaultwarden

**Use:** Evaluate a self-hosted Bitwarden-compatible secret store when the user explicitly wants managed credentials outside ACO knowledge.

**Avoid:** Never store passwords, recovery codes or API keys in ACO.md, prompts, Git or the resource registry; do not migrate secrets automatically.

**Checks:** External security-sensitive service. Review backup, TLS, updates, admin access, exposure, client compatibility and AGPL obligations before deployment.

Roles: `security_engineer`, `devops_engineer`, `office_administrator`.

Required capabilities when executing: server_deployment, security_review.

[Original ACO method](../playbooks/SECRETS-BOUNDARIES.md). External upstream content is not bundled. No execution tests performed.

## changedetection-io

**changedetection.io** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/dgtlmoon/changedetection.io

**Use:** Watch explicitly chosen public pages for meaningful changes such as calls, jobs, prices or release notes.

**Avoid:** Respect robots.txt/terms/access policies; do not monitor private/authenticated pages without authorization or convert every research target into a permanent watch.

**Checks:** External monitor; licensing/commercial terms have had public ambiguity, so review the current LICENSE and commercial terms for deployment. Scheduling requires a real running service.

Roles: `art_opportunities_scout`, `job_opportunity_scout`, `technical_researcher`, `automation_integration_engineer`.

Required capabilities when executing: server_deployment.

[Original ACO method](../playbooks/MONITORING-WATCHES.md). External upstream content is not bundled. No execution tests performed.

## localsend

**LocalSend** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/localsend/localsend

**Use:** Transfer approved files between nearby devices when a local-network route is preferable to cloud sharing.

**Avoid:** Do not assume the destination device is trusted, expose sensitive shares on untrusted networks, or treat transfer as archival backup.

**Checks:** External app. Verify device identity, network context, checksums for important media and receiving path.

Roles: `asset_manager`, `media_data_wrangler`, `office_administrator`.

Required capabilities when executing: local_execution.

[Original ACO method](../playbooks/FILE-TRANSFER-ARCHIVE.md). External upstream content is not bundled. No execution tests performed.
