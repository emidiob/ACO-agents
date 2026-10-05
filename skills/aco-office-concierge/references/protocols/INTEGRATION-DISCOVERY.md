# Integration discovery and adapter selection

ACO requests a capability; the host provides the implementation. Do not hardcode one provider when an equivalent authorized capability may be supplied by another host adapter.

## Selection order

For the exact requested capability/operation:
1. inspect caller/host-provided adapter inventory;
2. require exact capability coverage;
3. require the adapter to be available and, for remote services, actually connected;
4. require the operation to be in the adapter's authorized operation set;
5. require the adapter metadata to be verified for this environment;
6. prefer an explicitly requested adapter only when it is ready;
7. otherwise select the smallest already-authorized ready adapter using the host's declared priority;
8. if none is ready, use the capability fallback without asking the user to install/connect a tool unless the requested outcome itself requires that external service.

Documentation, a registry entry or a remembered past connection is not current adapter evidence.

## Provider switching

If the user explicitly chose a provider/account and it is denied or blocked, do not silently switch to another provider. A different provider may be used only when the task is provider-neutral and the available authorization covers it.

## Output

Adapter resolution returns readiness metadata only. It never performs the action. The execution protocol still binds approval to the exact final action packet and requires a provider receipt for consequential outcomes.
