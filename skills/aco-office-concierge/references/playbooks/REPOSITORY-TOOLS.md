# Repository understanding without data sprawl or access shortcuts

Start with authorized native repository reads and known file paths. Read the catalogue/README, trace the relevant modules and tests, and pin the actual commit. Do not send a whole repository to another service because the host could not find a file.

GitDiagram gives a candidate architecture map; DeepWiki gives generated explanatory navigation; Gitingest gives a text digest; GitMCP gives repository/document retrieval; github.dev is a browser editor, not a shell or test runtime. Their output is evidence to check against source—not authoritative proof of behavior or completeness.

For any hosted route, resolve public/proprietary/private ownership, excluded paths, secrets and explicit data-transfer approval. Even a publicly readable ACO repository retains its license: visibility is not a blanket transfer/redistribution permit. Prefer a scoped local digest when approved. Record excluded/truncated files and source revision; never claim the entire repo was read if it was not.

Agent Reach adapters need their own platform permissions and current capability inspection. Do not borrow browser cookies, use a proxy/alternate identity to bypass restrictions, disable security, or try an unsupported endpoint after a denial. A blocked source remains blocked.

LibreChat is a possible separate host/deployment, not a skill installed into ChatGPT. Shepherd is unresolved between projects until the user supplies the exact source. New hosts require explicit account/data/storage/security review, not automatic chat migration.

Return a bounded source map, citations to actual files, uncertainties and a concrete implementation/test plan. Save only durable conclusions and pointers in the existing project document. No full-repo dump or diagram archive per conversation by default.

Sources: [GitDiagram](https://gitdiagram.com/), [Gitingest](https://gitingest.com/), [DeepWiki](https://deepwiki.com/), [GitMCP](https://gitmcp.io/), [github.dev](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor), [Agent Reach](https://github.com/Panniantong/Agent-Reach), [LibreChat](https://github.com/danny-avila/LibreChat).
