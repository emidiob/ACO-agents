# Host adapters and execution receipts

ACO does not bundle a mandatory provider layer. The host may satisfy a capability through a native tool, connected integration, MCP server, local runtime or authorized API. The same ACO method can therefore run in ChatGPT, Codex or another approved host without pretending those environments expose identical tools.

## Adapter contract
A usable adapter declaration states:
- adapter identifier and kind;
- exact ACO capability IDs / operations it exposes;
- whether it is currently verified;
- a non-secret evidence reference for that verification;
- no embedded credentials.

A documentation link, registry entry or installed package is not proof that an authenticated capability is currently usable.

## Receipt contract
After an adapter call, preserve the narrowest outcome supported by evidence. A receipt identifies:
- `receipt_id`;
- task `scope_id`;
- `capability_id` and operation;
- SHA-256 of the exact approved action packet;
- outcome status;
- adapter ID;
- provider/artifact reference when a consequential terminal outcome is claimed;
- evidence references.

A receipt does not authorize another action and must not silently broaden scope. If an adapter times out or the provider outcome is ambiguous, record `unknown` and reconcile it before retrying.

## No fictional adapters
When an adapter is absent, return the prepared artifact/packet or execution instructions. Never simulate provider IDs, delivery receipts, successful uploads, publications, submissions or payments.
