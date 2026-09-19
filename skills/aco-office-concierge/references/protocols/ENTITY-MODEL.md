# Private entity model, schema 1

Organizations are the user's own businesses/organizations. Activities are business lines within one organization. Clients are counterparty relationships within one organization. Brands are owned by an organization or client. Projects have one canonical owner (organization, artist or career) and can reference several activities, one client and one brand. Matters belong to an owner, client or project.

Each entity record has: id, kind, stable key, display name, parent_id, owner_id, path or provider folder_id, context file reference, links, creation time and provenance. Do not put private IDs in public GitHub files.
Use generated stable IDs; never rely on display names alone. Two organizations may each have a client called “Studio North” with different IDs. Distinct clients can also share a label within one organization if given explicit different keys. Ask when the user cannot be matched unambiguously.

Allowed parents:
- organization/artist/career: workspace root;
- activity/client: organization;
- brand: organization or client;
- project: organization/artist/career;
- matter: organization/artist/career/client/project.

A project may span multiple activities in its owner's organization. It has one folder, not duplicates under every activity. Separate legal organizations are not merely two activities. Do not invent legal entity status, tax treatment or ownership from a brand name.

Reject cross-owner links by default. Cross-organization collaboration requires an explicitly approved shared-project record with a minimal information boundary, not copying one client's complete context into another organization. This release's local CLI deliberately refuses cross-owner links. Folder organization is not an ACL; use provider permissions and separate ChatGPT projects/workspaces when confidentiality requires it.

## Defaults
Create personal artist/career scopes only when requested. Create organizations, activities, clients and brands when they are needed, not a forest of empty examples. For a legal request, create one matter if needed and record unknown jurisdiction rather than assuming it.
Facts, current decisions, hypotheses, preferences and open questions remain separate. Declaring an entity name or approved root authorizes identity continuity, not unrestricted reading of every related record.
