# Reconstruct and transfer the complete motion

A reference image constrains a state; it does not specify the path into or out of that state. For source recreation or motion transfer, inspect the whole source temporally before finalizing the prompt. A few attractive keyframes are insufficient. Use playback when available; otherwise inspect dense chronological frame sequences, refine ambiguous intervals and disclose that playback/audio were not reviewed. Do not infer hidden hand movement from a before/after pair.

## Observe before translating

Follow each subject, manipulated object and the camera separately. Record meaningful transitions rather than every frame: anticipation/reach, contact, grip changes, support transfer, lift, translation, rotation, release and settling when actually present. Include stillness, pauses, speed changes and simultaneous actions. Distinguish camera movement from a subject moving through the frame. Preserve left/right coordinate conventions (subject's anatomical side versus screen direction); do not invent anatomy behind an occlusion.

For each event describe initial state → visible action → final state, actor, affected object, path/direction, orientation, contact/support and rhythm. Include only observable details; mark uncertainty and inspect more frames where it matters. Keep events overlapping when actions are simultaneous. Never collapse several observed steps into “picks up the object” or “copies the movement.”

Review the entire source duration, including opening and tail. Build `motion-plan.json` using the schema below. This is an observation record, not automatic motion tracking. An unknown interval must remain unresolved; do not mark it reviewed merely to satisfy a validator.

## Apply to the new video

Map every source actor/object to its target role before writing the prompt. For unchanged recreation the mapping preserves that entity. For a transformation, change appearance only as requested and explicitly apply each observed movement to its target. Check reach, limb count, scale, grip and contact against the new design. If the target cannot perform an action, resolve the incompatibility rather than dropping it silently.

Record source times and target times separately. Preserve pace by default. If a different duration is requested, retime all dependent movements coherently and document the mapping. Do not invent a cut to bridge a missing action. An intentionally omitted movement needs the user's requested change and its reason recorded.

Write the final prompt chronologically, explicitly naming who moves, what they contact, how objects travel and how the camera behaves. Integrate simultaneous tracks naturally. Keep the movement sequence even when shortening appearance prose. Use observed times as a production guide; exact timing is not a provider guarantee. Do not paste internal IDs or the whole JSON into the user-facing prompt.

## Motion record

Top-level fields:
- `source_duration_seconds`, `target_duration_seconds`: positive numbers.
- `reviewed_intervals`: pairs of source seconds covering the duration actually inspected.
- `entities`: mapping of stable source names to target descriptions, including `camera`.
- `events`: chronological records (overlaps allowed) with the fields below.

Each event has `id`, `actor` (key in entities), `track` (`subject`, `object` or `camera`), `source_interval` and `target_interval` (start/end pairs), `observed` (specific initial/action/final account), `target_action` (the same action applied to the target), `evidence` (actual local inspected frame filenames from the reference map), and `certainty` (`observed` or `uncertain`). For transferred events, `prompt_excerpt` is an exact excerpt from `shot-prompt.txt` expressing that action. For an intentional omission use `disposition: omitted`, `omission_reason` and `requested_change` instead; omit only within the user's requested changes. The normal disposition is `transfer`.

Record a static camera explicitly when observed. Subject and object tracks may overlap; an object moved by a hand should include its path/contact either in the subject event or a separate object event. Avoid redundant rows that add no observable information. Add holds for actual pauses, not to conceal uninspected gaps. Evidence can include additional analysis frames beyond the minimal provider upload set; record those as references with purpose and time.

Run `python3 scripts/check_reference_pack.py TASK_DIRECTORY`. The checker now requires this motion record: it detects missing duration coverage, unknown actors, absent evidence, unresolved events and prompt excerpts lost during editing. It checks declared correspondence, not the truth/completeness of observations or semantic equivalence of a generic sentence. Manually compare the source, motion record and final prompt event by event. A source action absent from the record cannot be detected by this script.

## Review an actual result

If a generated video is available, inspect the corresponding intervals and compare order, path, orientation, contact, pace, camera and final state. Report each missing/reversed/changed movement and repair the smallest relevant scope. Never claim the movement has been reproduced from prompt coverage alone. Generation and external uploads remain separate from local reference preparation.
