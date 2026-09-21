# Official references checked for this release

Checked 19 September 2026. UI, availability and configuration formats can change. Follow the actual host/tool schema rather than assuming a menu exists.

- Codex skills/discovery: https://developers.openai.com/codex/skills
- Codex custom agent TOML scope and required fields: https://developers.openai.com/codex/subagents
- Codex project instructions: https://developers.openai.com/codex/guides/agents-md
- Codex MCP support: https://developers.openai.com/codex/mcp
- ChatGPT GitHub connection: https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt
- ChatGPT Projects: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- Google Docs batchUpdate / WriteControl requiredRevisionId: https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/batchUpdate
- Google Drive generated file IDs for retryable creation: https://developers.google.com/workspace/drive/api/reference/rest/v3/files/generateIds
- Google Drive upload types: https://developers.google.com/workspace/drive/api/guides/manage-uploads
- Python downloads: https://www.python.org/downloads/

Some OpenAI URLs redirect to the current ChatGPT Learn documentation. No provider availability is inferred solely from these pages: verify the current account's actual tools and permissions. The optional bridge's HTTP implementation has fake-provider tests, not an authenticated Google end-to-end certification.

GitHub Actions versions checked 2026-09-19: https://github.com/actions/checkout/releases and https://github.com/actions/setup-python. CI uses tagged v7.0.1/v7.0.0 releases with contents:read and no persisted checkout credentials; maintainers should review dependencies periodically.


## v0.4.0 methods and capability checks

Checked 2026-09-19; re-check when executing version-sensitive work.

- OpenAI skill structure and local discovery: https://developers.openai.com/codex/skills (may redirect to the current official Learn documentation).
- OpenAI custom agents and scope: https://developers.openai.com/pt-BR/docs/agent-configuration/subagents (official translated page; use English equivalent when available).
- OpenAI MCP configuration/capability: https://developers.openai.com/codex/mcp.
- ComfyUI routes, object_info and prompt queue/history: https://docs.comfy.org/development/comfyui-server/comms_routes.
- ComfyUI custom-node installation/environment guidance: https://docs.comfy.org/installation/install_custom_node.
- ComfyUI workflow environment troubleshooting: https://support.comfy.org/articles/1536450065-missing-nodes-workflow-won-t-load.
- Academy ACES color/transform documentation: https://docs.acescentral.com/.
- W3C EPUB 3.3 and EPUB Accessibility 1.1 specifications: https://www.w3.org/publishing/epub/.

The method cards are original task instructions, not copied technical manuals. They require the real application's current documentation, schemas and test evidence. No claim is made that a named provider is installed or that outbound calling exists in every communications app. WhatsApp/MCP adapters are intentionally discovered at runtime and not bundled.

Existing CI release tags were checked against upstream on 2026-09-19: actions/checkout v7.0.1 (https://github.com/actions/checkout/releases) and actions/setup-python v7.0.0 (https://github.com/actions/setup-python/actions/runs/29714253785). This verifies release existence, not completion of this repository’s CI jobs.

## v0.5.2 optional resource intake

Reviewed 20 September 2026. ACO includes only original selection/method notes; it does not vendor these projects. Re-check current licenses, versions and service terms before installation or reuse.

- https://github.com/trekhleb/javascript-algorithms
- https://github.com/30-seconds/30-seconds-of-code
- https://github.com/public-apis/public-apis
- https://github.com/langflow-ai/langflow
- https://github.com/every-app/open-seo
- https://github.com/ayghri/i-have-adhd
- https://github.com/petergyang/no-ai-slop
- https://github.com/lfnovo/open-notebook
- https://github.com/louislam/uptime-kuma
- https://github.com/excalidraw/excalidraw
- https://github.com/dani-garcia/vaultwarden
- https://github.com/dgtlmoon/changedetection.io
- https://github.com/localsend/localsend
- https://github.com/mikf/gallery-dl
- https://github.com/reactive-resume/reactive-resume
- https://github.com/searxng/searxng
- https://github.com/imputnet/cobalt
- https://github.com/langgenius/dify
- https://github.com/unclecode/crawl4ai
- https://github.com/browser-use/browser-use
- https://github.com/getmaxun/maxun
- https://github.com/All-Hands-AI/OpenHands

The registry distinguishes learned ACO methods from external software. Skill concepts are rewritten as original ACO procedures; software remains an optional external capability.
