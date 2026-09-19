# Optional integrations: capabilities, not promises

ACO is still a skill library. It does not bundle, auto-connect or proxy Gmail, Drive, WhatsApp, telephony, calendars, bank accounts, production software or publishing systems. In each host, inspect current available tools and their exact schemas. Discover a missing integration when the task would benefit; if none is available or the user declines, give the useful draft/file/manual handoff.

| Work | Inspect for | Without the action |
|---|---|---|
| Inbox/email | account identity, full thread read, draft action, send action, receipt | reply text in chat |
| WhatsApp/MCP | provider health, resolved contact/chat/group, text/media send, outcome lookup | exact message to paste |
| Telephone | outbound dialing AND call handling, identity/disclosure, number, bounds, receipt | call and voicemail script |
| Calendar | timezone, availability, create/update/invite | invitation proposal |
| CRM | scoped contact/deal read/write, duplicate lookup, access | structured update draft |
| Project tracking | task read/create/update, assignee resolution, status evidence | task list or import packet |
| Finance | approved accounting records, reconciliations; payments are separately controlled | budget/invoice/adviser packet |
| Production | DCC/CLI/API tools, actual media, explicit versions/paths, execution receipts | treatment, edit list, retouch/grade/render instructions |
| ComfyUI | real node/model inventory, graph format, queue/history and available GPU | untested graph/blueprint and dependency checklist |
| Publishing | CMS/design/export/EPUB/prepress/distributor actions | publish-ready draft/files and handoff |

WhatsApp connections vary. Never invent a function named after a remembered provider; use discovered actions. Calling through WhatsApp is separate from sending a text. Reading call notes is not dialing. No automatic group creation, bulk outreach, consent bypass or cross-channel retries.

For an authorized send: verify scope + account + recipient + content/attachments + user approval; inspect duplicate/uncertain prior attempts; invoke actual tool; report precise result. Existing clear authorization need not be asked again. A provider error is not permission to switch services. A timeout may mean success or failure: reconcile first.

The bundled `action-plan` is an **offline planner**. Its authorization fields are supplied assertions, not an access-control system or proof of user consent. It never sends messages or makes calls. Host permissions and real provider scopes remain decisive.

No sample phone numbers, tokens, contact IDs or user Drive folders are configured in the public repository. Credentials belong in the provider/host's approved secret storage, never in chat or Git. Active recurring delivery requires a separate real scheduler, explicitly authorized.
