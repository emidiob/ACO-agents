# Repeatable setup — no duplicate folders, no resetting user content

## Before writes
Confirm that the user authorized initialization in the selected location. Check actual read/create/update tools and provider account. If write is unavailable, provide an initialization packet and label NOT CREATED; do not simulate completion.
Read current root metadata and immediate children. Do not create a second root because search indexing is delayed. For >100 children or paginated search, continue using provider tokens until discovery is complete.

## Base structure
Create or reuse only the missing elements:

```
ACO — Art & Commerce Office/
  KNOWLEDGE-INDEX                  # native Doc or Markdown; one canonical ID
  00-System/
    REGISTRY                      # machine-readable JSON in raw file or native Doc
    Setup-Journal/
    Sync-Receipts/
  Personal/
  Organizations/
  Archive/
```

The root index links to the registry and actual entity folders. It should not duplicate all private project content. Registry schema_version=1, authority=drive|local, namespace=<generated UUID>, entities={...}, provider_locations={...}. Provider file IDs and content/revision checks belong only to private records.

## Procedure
1. Read existing registry/index and check schema version. Unknown schemas or inconsistent duplicates are conflicts, not permission to wipe anything.
2. Assign a setup operation ID and journal each intended logical object and actual provider ID returned. Reuse a saved ID, not an invented one.
3. Before each create, query the exact parent and name/metadata key. Zero matches: create. One: validate type and reuse. Several: report conflict and preserve all until reconciled.
4. After each creation, read metadata/content back. Record created, reused, failed, or unverified. Never emit all-success from a partially failed batch.
5. Create the root control files once. Preserve user content on every re-run. Use provider revision control for updates when available.
6. If interrupted, resume the journal and repeat exact reads. Do not make another set of folders.
7. When an entity is first needed, create its Context, History/Events, History/Sessions, History/Proposals, History/ContextVersions and Handoffs. Initialize WORK-LOG, DECISIONS, OPEN-LOOPS and CONTEXT-CHANGELOG as views; no invented history. Add Applications for career or a matter index only when needed.
8. Add the entity ID, parent/owner and provider locations to the registry. Verify the registry update; a folder created without a registry entry remains a recoverable pending step.
9. Return a brief summary with actual links/IDs in the private session and setup outcome. The user should not need to create folders or type IDs manually.

## Concurrency
Drive names are not unique and ordinary search-then-create is not atomic. Only one setup writer may initialize/restructure a root at a time. Re-read after creates to detect collisions. Never claim a distributed lock from a prompt or folder name. Concurrent ordinary work uses separate session/event IDs. Native Docs updates should use requiredRevisionId where the connector exposes it. Raw files without conditional writes need single-writer coordination or an immutable proposal, not optimistic overwrites.

## Existing legacy ACO roots
Discover first. Preserve documents, IDs and content. Move known records into the appropriate personal/organization scope only after resolving their owner. Archive redundant empty indices instead of deleting useful content. Unknown ownership goes into a review queue; no automatic classification of private legal/client material. Journal old/new parent IDs and provide rollback instructions.

## Local execution
The supplied Python CLI implements repeatable local bootstrap and entity creation with OS locks and atomic writes. It does not itself authenticate Google Drive. In a chat with connected Drive tools, execute the same protocol through those tools. The optional REST bridge handles immutable session events only, not wholesale mirroring of context.
