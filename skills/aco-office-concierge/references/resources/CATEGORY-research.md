# Research resources

Optional catalogue, not an installation list. Consult current source and actual host capabilities.

## agent-reach

**Agent Reach** · integration · source_reviewed · reviewed 2026-09-20

Source: https://github.com/Panniantong/Agent-Reach

**Use:** Evaluate allowed source-specific retrieval adapters when native connected tools cannot do a permitted task.

**Avoid:** Never bypass access controls, borrow unrelated cookies, weaken security or rotate identities to evade restrictions.

**Checks:** Individual platform adapters have separate auth, terms, costs and breakage risks; no blanket free/unlimited claim.

Roles: `technical_researcher`, `automation_integration_engineer`, `mcp_integration_reviewer`.

Required capabilities when executing: local_execution.

[Original ACO method](../playbooks/REPOSITORY-TOOLS.md). External upstream content is not bundled. No execution tests performed.

## gitdiagram

**GitDiagram** · service · source_reviewed · reviewed 2026-09-20

Source: https://gitdiagram.com/

**Use:** Get an exploratory architecture view of an authorized public codebase.

**Avoid:** Generated diagrams are hypotheses; do not upload private/proprietary repos without explicit owner approval.

**Checks:** Hosted service capability, model cost, retention and actual commit coverage must be checked per use.

Roles: `software_architect`, `technical_researcher`.

Required capabilities when executing: external_service.

[Original ACO method](../playbooks/REPOSITORY-TOOLS.md). External upstream content is not bundled. No execution tests performed.

## gitingest

**Gitingest** · service · source_reviewed · reviewed 2026-09-20

Source: https://gitingest.com/

**Use:** Prepare a bounded text digest; prefer local, filtered use for authorized code.

**Avoid:** Do not send an entire private repository, secrets, build outputs or irrelevant context to a hosted endpoint.

**Checks:** Resolve local versus hosted route first; digest coverage/truncation must be recorded. Not an execution environment.

Roles: `technical_researcher`, `code_reviewer`.

Required capabilities when executing: external_service.

[Original ACO method](../playbooks/REPOSITORY-TOOLS.md). External upstream content is not bundled. No execution tests performed.

## github-dev

**github.dev editor** · feature · source_reviewed · reviewed 2026-09-20

Source: https://docs.github.com/en/codespaces/the-githubdev-web-based-editor

**Use:** Edit authorized repository files in the browser using GitHub’s web editor.

**Avoid:** Not a full runtime, shell or proof a build/test ran; user permissions still apply.

**Checks:** Browser editing is distinct from Codespaces and locally running VS Code.

Roles: `frontend_engineer`, `documentation_writer`.

Required capabilities when executing: browser_editor.

[Original ACO method](../playbooks/REPOSITORY-TOOLS.md). External upstream content is not bundled. No execution tests performed.

## deepwiki

**DeepWiki** · service · source_reviewed · reviewed 2026-09-20

Source: https://deepwiki.com/

**Use:** Use generated codebase explanations as navigation aids then verify against actual source/ref.

**Avoid:** Not authoritative documentation; not all repositories/branches are indexed. Never upload private code by inference.

**Checks:** Check index commit/date, access, retention and source evidence. Native repository reads take precedence.

Roles: `technical_researcher`, `software_architect`.

Required capabilities when executing: external_service.

[Original ACO method](../playbooks/REPOSITORY-TOOLS.md). External upstream content is not bundled. No execution tests performed.

## gitmcp

**GitMCP** · integration · source_reviewed · reviewed 2026-09-20

Source: https://gitmcp.io/

**Use:** Query relevant repository documentation through a separately configured supported MCP endpoint.

**Avoid:** Read/document retrieval does not grant push, shell or private repo access. No automatic account-token sharing.

**Checks:** Inspect endpoint identity, permissions, indexed refs and privacy; prefer existing authorized GitHub tools.

Roles: `technical_researcher`, `mcp_integration_reviewer`.

Required capabilities when executing: mcp_repository_read.

[Original ACO method](../playbooks/REPOSITORY-TOOLS.md). External upstream content is not bundled. No execution tests performed.

## open-notebook

**Open Notebook** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/lfnovo/open-notebook

**Use:** Create a bounded research workspace around supplied PDFs, videos, sites and notes when local/self-hosted source-grounded exploration helps.

**Avoid:** Do not duplicate ACO canonical memory, ingest unrelated private archives, or treat generated summaries/podcasts as source evidence.

**Checks:** External research application. Preserve citations/provenance and keep ACO canonical decisions in Compact Memory rather than duplicating every note.

Roles: `studio_research_librarian`, `knowledge_architect`, `art_researcher`, `research_director`.

Required capabilities when executing: local_execution_or_server_deployment.

[Original ACO method](../playbooks/RESEARCH-KNOWLEDGE-WORKSPACE.md). External upstream content is not bundled. No execution tests performed.

## searxng

**SearXNG** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/searxng/searxng

**Use:** Use a self-hosted metasearch route when broader source discovery and local control are worth the infrastructure.

**Avoid:** Do not claim end-to-end anonymity: upstream engines, instance configuration and network providers may still observe requests; verify sources individually.

**Checks:** External metasearch service. Search results are discovery, not evidence; preserve final citations to original sources.

Roles: `technical_researcher`, `art_researcher`, `job_market_researcher`, `press_reputation_researcher`.

Required capabilities when executing: server_deployment.

[Original ACO method](../playbooks/RESEARCH-KNOWLEDGE-WORKSPACE.md). External upstream content is not bundled. No execution tests performed.

## crawl4ai

**Crawl4AI** · library · source_reviewed · reviewed 2026-09-20

Source: https://github.com/unclecode/crawl4ai

**Use:** Crawl authorized web content into structured/LLM-ready material when a repeatable code-based extraction route is appropriate.

**Avoid:** Respect robots.txt, terms, rate limits and sensitive-data boundaries; do not crawl broadly when a normal page fetch/search answers the question.

**Checks:** External crawler. Current project documents Apache-2.0 plus attribution guidance; verify the exact version and security advisories before deployment.

Roles: `technical_researcher`, `content_researcher`, `data_engineer`, `seo_content_researcher`.

Required capabilities when executing: local_execution_or_server_deployment.

[Original ACO method](../playbooks/WEB-DATA-EXTRACTION.md). External upstream content is not bundled. No execution tests performed.

## maxun

**Maxun** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/getmaxun/maxun

**Use:** Create structured extraction jobs/APIs for authorized sites when a no-code scraper is operationally useful.

**Avoid:** Do not scrape protected/private data without authorization or use extraction output as verified truth without sampling and provenance.

**Checks:** External no-code scraping/crawling platform; repository states AGPLv3. Review auth handling, OCR, storage and MCP access before deployment.

Roles: `lead_qualification_researcher`, `data_engineer`, `business_analyst`, `content_researcher`.

Required capabilities when executing: server_deployment.

[Original ACO method](../playbooks/WEB-DATA-EXTRACTION.md). External upstream content is not bundled. No execution tests performed.

## zotero

**Zotero** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/zotero/zotero

**Use:** Maintain citations, reading notes and bibliography in an existing authorized library.

**Avoid:** No Zotero connector or credentials are bundled. Do not duplicate the full library on Drive or infer permission to sync private attachments.

**Checks:** No Zotero connector or credentials are bundled. Do not duplicate the full library on Drive or infer permission to sync private attachments.

Roles: `studio_research_librarian`, `art_researcher`, `art_historian`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/ARTISTIC-RESEARCH-AND-SOURCES.md). External upstream content is not bundled. No execution tests performed.

## tropy

**Tropy** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/tropy/tropy

**Use:** Describe and annotate photographed archival documents and field-research material.

**Avoid:** Use for substantial archival-image research, not as mandatory overhead. Distinguish document, photograph, rights and source location.

**Checks:** Use for substantial archival-image research, not as mandatory overhead. Distinguish document, photograph, rights and source location.

Roles: `studio_research_librarian`, `practice_archivist`, `art_researcher`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/ARTISTIC-RESEARCH-AND-SOURCES.md). External upstream content is not bundled. No execution tests performed.

## mirador

**Mirador / IIIF viewer** · library · source_reviewed · reviewed 2026-09-20

Source: https://github.com/ProjectMirador/mirador

**Use:** Compare and annotate actual IIIF image sources side by side.

**Avoid:** A manifest does not confer copyright permission. Verify image/service availability and preserve source attribution.

**Checks:** A manifest does not confer copyright permission. Verify image/service availability and preserve source attribution.

Roles: `curator`, `art_historian`, `art_researcher`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/ARTISTIC-RESEARCH-AND-SOURCES.md). External upstream content is not bundled. No execution tests performed.

## met-open-access

**The Met Open Access** · dataset · source_reviewed · reviewed 2026-09-20

Source: https://github.com/metmuseum/openaccess

**Use:** Find institutional collection records and eligible open images for documented research.

**Avoid:** Check item-level rights and image availability; collection metadata access is not a blanket licence for every depicted work or person.

**Checks:** Check item-level rights and image availability; collection metadata access is not a blanket licence for every depicted work or person.

Roles: `art_researcher`, `art_historian`, `curator`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/ARTISTIC-RESEARCH-AND-SOURCES.md). External upstream content is not bundled. No execution tests performed.

## getty-vocabularies

**Getty Vocabularies** · reference · source_reviewed · reviewed 2026-09-20

Source: https://www.getty.edu/research/tools/vocabularies/

**Use:** Disambiguate artist/place/material terms where controlled metadata is useful.

**Avoid:** Retain identifiers and source dates; preserve the artist’s own description. Confirm current API/data terms rather than assuming an endpoint migration.

**Checks:** Retain identifiers and source dates; preserve the artist’s own description. Confirm current API/data terms rather than assuming an endpoint migration.

Roles: `practice_archivist`, `art_historian`, `collection_inventory_manager`.

Required capabilities when executing: none declared; inspect the actual task/tool.

[Original ACO method](../playbooks/ART-ARCHIVE-AND-PRESERVATION.md). External upstream content is not bundled. No execution tests performed.
