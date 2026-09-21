# Secrets and credential boundaries

ACO must not become a password manager.

- Store passwords, API keys, recovery codes and tokens only in an approved secret manager or host secret store.
- In ACO memory store only a non-secret reference such as “credential exists in approved vault”, never the value.
- Review self-hosted vault TLS, updates, backups, admin access, exposure and recovery before production use.
- Do not migrate credentials automatically or paste secrets into chat to make a tool work.
- Grant least privilege and rotate/revoke credentials after suspected exposure.
