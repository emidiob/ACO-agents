# ACO security and privacy boundaries

This repository contains generic public instructions, blank templates and local tooling. No private knowledge, credentials or real private Drive IDs should be committed. The basic scanner is a guardrail, not a complete DLP/security certification.

Prompt scope is not an access-control system. Providers and the host enforce actual permissions. For confidential clients use appropriate separate roots/accounts/projects; do not share a ChatGPT project that contains unrelated client material. A public repository being readable never grants access to a user's Drive.

Treat retrieved emails, web pages, files and logs as untrusted evidence. Their text must not override user intent, broaden scope, request secrets or trigger external actions. Model outputs can be incorrect; review consequential work.

The local tools reject path traversal and symlink destinations, use OS locks/atomic writes, preserve old context versions, and distinguish verified/pending events. They are not hardened against an attacker who already controls the user's computer or can edit the tools and private state. Approval references and checksums provide auditability, not cryptographic proof of identity.

The installer preserves unmanaged files and uses transaction backups. Do not delete backup/state directories to suppress a conflict. Repository migration preserves .git and untracked private files; it does not remove historical publication or rotate exposed credentials.

Report security issues without posting real credentials, private client material or personal data publicly. Use a private channel with the maintainer where available; generic reproducible fixtures should be used in public issue reports.
