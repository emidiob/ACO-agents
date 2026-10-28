# Select a generation mode

Choose the operation from the requested change, not from a preferred model. Mode names below describe tasks; providers may name or implement them differently.

| Request | Inputs to prepare | What the prompt controls |
|---|---|---|
| New shot from an idea | A concise shot brief; optional approved design images | Subject action, environment, camera and sound |
| Animate a still | The inspected still | Motion and end state while retaining the visual design |
| Recreate a clip unchanged | Source clip; source frames at decisive moments when accepted | Preservation, action order and visual continuity |
| Transfer a performance | Motion source plus target identity/design references | Which source motion transfers to which subject |
| Change one element | Source plus precise region/object change and any replacement reference | A bounded edit, with surrounding action retained |
| Connect two states | Inspected starting and ending images | Plausible transition and what must match at each end |
| Continue a clip | Source tail and desired continuation | Boundary continuity, ongoing motion and next event |
| Several shots | Per-shot brief, durations, references and transition plan | Shot order, continuity and explicit transitions |

## Unchanged recreation

Do not invent a new face or redesign the set. Prepare anchors directly from the source: opening composition, major action change, contact/occlusion and ending. One frame may serve several purposes in a simple shot. If the provider cannot accept video guidance, disclose that still-guided animation is a different and less constrained operation. A prompt requesting exactness is not evidence of exact reproduction.

## Performance or identity change

List source subjects by visible position and assign each requested target once. Distinguish movement, identity, wardrobe and scene references. Preserve body scale and staging unless the user requests otherwise. Back-facing moments do not need a fabricated face. A large pose or silhouette change may require reference stills matching those moments. For a requested visual transformation, create the necessary stills with the available image tool and inspect them. Reuse the verified design consistently at subsequent source moments. Ask only for missing target design information or an actual tool-required permission; a prompt-only specification is a fallback for a concrete blocker, not the default deliverable.

## Editing and continuation

An object replacement should not silently become a full-scene regeneration. Record what may change, the first and last affected moment and what must stay continuous. At an extension boundary, match pose, movement direction, camera speed, exposure and sound. Do not invent a provider's masking or extension feature.

## Multiple shots

A cut is a deliberate transition, not an action beat. Give each shot its own framing, action, starting state, ending state and reference bindings. Keep character and object continuity across shots. Use separate generations when the interface cannot express the requested sequence reliably. Do not split a continuous source simply to fit a template.
