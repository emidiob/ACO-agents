# ACO prompt notation

This is an authoring format, not a provider API or a claim that special punctuation is understood by a model. Keep two layers: the production brief below and the final prompt translated for the selected interface. Omit fields that do not help the task.

## Reference bindings

Assign readable local labels such as `source_clip`, `start_anchor`, `turn_anchor`, `person_target`, `surface_target`, and `sound_source`. Each binding contains:

- Actual filename and, for extracted frames, source timestamp.
- Property to use: appearance, movement, composition, texture, identity or sound.
- Properties that must not transfer, when there is a conflict.
- Inspection status: viewed, listened, metadata-only or user-described.

Do not put an invented upload identifier into a runnable prompt. If a verified interface creates numbered image/video tags, map local labels to those exact tags after establishing upload order. A reference used for identity does not automatically define pose, expression or background. For an unchanged recreation the source can legitimately govern all visual properties.

## Shot record

```
PURPOSE: what the result must accomplish
SOURCE BINDINGS: existing files and their allowed influence
CONTINUITY: properties to retain; requested differences
ACTION: initial state -> observable change -> final state
CAMERA: framing and orientation; movement and its trigger
APPEARANCE: subject, environment, illumination and finish
SOUND: retained source / specified new sound / silence / unresolved
```

For time-sensitive shots, add a small event table with `start`, `end`, `action`, `anchor` and `certainty`. Derive source times from inspected frames; distinguish observed times from requested generation times. Cover the requested duration without accidental overlaps or gaps. For a continuous take, adjacent intervals describe one ongoing action rather than implied cuts.

## Compile the prompt

Open with the intended transformation and the role of the supplied source. Describe the action with a clear start and finish, then camera behavior, appearance and sound. Identify the few properties most likely to drift. Keep setting values in the interface fields when supported rather than burying them in prose. End with the requested final state; looping or continuation may need a different end state.

Use concrete clauses: “the right hand stays beneath the tray until it is set down” is stronger guidance than “perfect realism.” Do not assert a lens, camera path or emotion that the source does not establish. Use image evidence to constrain grips and occlusions instead of trying to describe every finger.

## Sound, speech and visible writing

These are separate tracks in the brief:

- **Ambience:** continuous environmental bed and whether it comes from the source.
- **Events:** sound cue, corresponding action and approximate position in the shot.
- **Speech:** speaker, exact words, language, delivery and visible speaking interval.
- **Music:** desired role or explicitly absent; do not add it by default.
- **On-screen writing:** exact text, placement, interval and whether it will be added in editing.

Translate these into documented provider fields or ordinary language. Do not assume parentheses, angle brackets, braces or other punctuation have special meaning. Do not claim an uploaded video implies audio retention. For exact original sound, plan to preserve the original audio track in editing when requested; never claim that edit already exists.

## Settings verification

Record provider, model, interface (web/API/local graph), current evidence source and date. Check the selected mode's input types, file limits, duration, aspect, resolution, frame rate, audio behavior and any endpoint-frame or seed controls. Use official documentation or the actual interface. Repository examples are prompting ideas, not proof of today's controls. Unsupported precision stays a production target, not a promised setting.
