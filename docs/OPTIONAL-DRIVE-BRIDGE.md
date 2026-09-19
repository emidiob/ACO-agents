# Optional local Drive event bridge — advanced, not required

Most ChatGPT users should use separately connected Drive tools and the normal ACO protocols. The Python bridge exists for a local Codex environment that has no such writable tool. It is an event transport, not a general Drive synchronization service.

Requirements: an OAuth access token obtained locally through your own authorized Google application/tooling, with permissions adequate to the chosen folder and file creation. Do not paste tokens into ChatGPT, GitHub, shell history or source files. ACO does not ship a client secret, offer an OAuth consent screen or acquire access by itself. Account authorization, token refresh and Google API enablement must be configured outside this bridge. A short-lived token is read from ACO_GOOGLE_ACCESS_TOKEN in the local process environment only.

`drive-bind` requires an explicit root ID and approval reference. It reads that root and searches only direct scoped children. It creates/reuses “ACO Session Events”, records the binding privately, and refuses silent rebinding.

`drive-sync` sends explicit pending event JSON only. It creates a provider-generated ID before upload and journals it locally, reads back exact payload bytes, and writes a receipt after verification. It neither uploads your entire knowledge directory nor overwrites canonical context. A token expiration/network failure preserves pending data. Retry after locally refreshing authorization. Do not work around an access denial with a broader token unless the user deliberately approves a changed access policy.

Safety limits: no distributed unique-name constraint; serialize initial setup. Duplicates and differing remote event content are conflicts. Already-synced events are rechecked when sync is invoked again. There is no polling/watch process or automatic timer. The shipped tests use a fake provider and do not validate a real Google account; perform a disposable private-root smoke test before real use.

See SOURCES.md for Google's official file ID and upload documentation. Prefer native Docs revision control through connected tools for mutable canonical documents.
