> Current release is v0.5.1. Follow the new package README update instructions; Compact Memory affects future storage, not automatic deletion of existing private data.

# Migration from ACO plugin v0.2.1

The known previous repository is a generic public source package. The new release removes active plugin manifests, marketplace metadata and submission/privacy/terms documents specific to directory distribution. It keeps the generic role knowledge, now canonical in one Markdown definition per role with generated prefixed TOMLs. ACO v0.4.3 intentionally replaces the current-release MIT license with the ACO Proprietary Source-Available License v1.0; repository history is preserved.

Do not manually delete everything. The migration script checks recorded SHA-256 fingerprints of known legacy paths and the new release manifest. It refuses custom modified content, dirty tracked files and untracked collisions. It preserves unrelated files and history and creates a backup branch before staging changes. The source ZIP must be extracted outside the existing repository.

After migration, run all tests/validation and inspect the staged diff before committing. Push is a separately authorized operation; no force push. The v0.4.3 license change is intentional and must appear clearly in the staged diff. Earlier releases lawfully distributed under another license remain governed by the license that accompanied those releases. Previously published Git history remains; deleting a current file is not secret removal from historical commits. Real leaked credentials require rotation and a separately reviewed remediation, not this migration.

Old globally installed unprefixed native agents are not silently deleted. New agents are named aco_*. To remove old duplicates, first compare them to the old definitions, back up locally modified files, and remove only confirmed obsolete ACO profiles with user authorization. Never bulk-delete ~/.codex/agents.

Drive migration is separately journaled by the bootstrap protocol. Existing files keep their IDs/content where moved. Unknown ownership goes to a review queue. Do not replace actual context with blank templates.
