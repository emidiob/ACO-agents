# Entities are identity records, not a requirement to create folders

Default layout is Compact Memory schema 2. Organizations are the user's actual operating organizations; artist and career are personal owner scopes. Activity means business line; client means a counterparty relationship; brand belongs to an organization/client; project has one owner and may reference several activities, one client and one brand; a matter has an explicit restricted scope when necessary.

Stable IDs disambiguate identical names. Do not infer legal status or ownership from labels. Keep session scope local to that request; no global current client. Reject cross-owner relationships and misleading brand/client links. A cross-organization shared project needs explicit boundary design; the supplied local backend rejects cross-owner links.

A pipeline item has a stable row ID, kind, status, title, concise notes, source and next action, not an entity folder. A proposed artwork, possible client, application, experiment or unaccepted collaboration cannot be registered as a project merely because it was discussed. Record nothing persistently if it is not worth retaining.

Promotion needs explicit user commitment, evidenced external activation or import of a known real entity. Activation is separate from document creation: small active items remain sections. Only genuine independence, scale or confidentiality justifies another ACO.md. No placeholder histories, event/session folders, applications directory for every application or quarterly archive by default.

Canonical index: logical ID, kind, parent/owner, actual canonical file/section reference and activation provenance. The local CLI maintains compact JSON metadata inside the existing index; detailed sessions and retries are private local state outside knowledge. Do not expose these IDs through the public repo.

Folder separation is not access control. Do not mix unrelated clients or restricted HR/legal/financial content into an owner document just to reduce file count. Use separately permissioned records when needed. Preserve primary documents and link them; compact memory does not compress an accounting ledger or replace contracts.
