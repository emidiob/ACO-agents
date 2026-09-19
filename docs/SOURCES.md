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
