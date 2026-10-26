# Deliver references before the prompt

A source-guided request needs usable images, not merely a list of images somebody could make. Complete the reference work first, unless the user explicitly requests only text. Keep the writing original and tailored to the actual source.

## Produce the files

1. Inspect the supplied video and select moments that expose its important changes. Include the start/end when they constrain the result and inspect contact/occlusion moments more closely. Extract actual frame files with the local helper or available media tools into a task directory outside the ACO library. Do not stop after printing metadata.
2. Open the extracted images. Remove redundant choices from the delivery selection without deleting source material. Keep a record of each selected frame's timestamp. Create a contact sheet for navigation; keep the full-size individual images for use as references.
3. For an unchanged recreation, those original frames are the reference images. Do not generate lookalikes, invent faces that are turned away, or require new character sheets.
4. For a requested change, use the available image-generation/editing tool to make a reference showing that change in an inspected source composition. Inspect the result before continuing. Preserve source pose, screen position, contact and environment except where the user explicitly changes them. Use the verified transformed appearance consistently for the other necessary moments; inspect each result and repair specific discrepancies. A proposed image description does not count as an image.
5. Where identity detail is genuinely needed and visible, provide an appropriate detail reference from the verified material. Do not fabricate a frontal face for an entirely back-facing performance. Use the available authorized image tool for image transformations.

## What to show

Show the reference contact sheet and clickable links to the selected individual images, ordered by source time. For a transformation, make source/result correspondence easy to inspect. The compact map identifies filename, timestamp, role, and whether the image is extracted or edited/generated. Do not claim an upload has happened.

The final prompt should name the prepared references using the chosen interface's verified bindings. If that interface is not chosen yet, use filenames and leave only the provider-specific conversion unresolved. A missing model name does not stop reference creation.

## Completion and blockers

References are delivered when the files exist, have been visually inspected, and are accessible to the user. State any remaining discrepancy rather than claiming an unobserved match. If the target appearance is unspecified, ask for that missing design/reference while preparing source frames. If an image tool fails or is unavailable, report the specific limitation and deliver the work that did complete. Do not silently substitute a generic prompt for unfinished images.

Do not render video or upload the user's files externally merely to prepare this package. Image-tool actions must remain within the requested transformation and actual host permissions. A still-generation failure is not permission to use another paid service without the applicable authorization.

## Run the complete local preparation

Use `python3 scripts/inspect_video.py SOURCE --output NEW_TASK_DIRECTORY` from the skill folder. It creates a chronological overview of up to 24 actual frames including the endpoints, candidate cut times, full-size selected frames, a reference strip and a draft `reference-map.json`. The default selection is exploratory, not a claim that evenly spaced frames capture every meaningful pose. After reviewing the overview, use `--times` with observed action moments in a new directory when needed. The report records actual decoded-frame timestamps separately from requested times, including for variable frame rates.

Open the overview and selected images. Check potential cuts, grip changes, occlusions and the final state; refine uncertain intervals. Set the reference-map intent, describe each image's actual purpose and mark `visually_reviewed` only after inspection. Preserve the provided SHA-256 values; update hashes after an intentional image edit and repeat its visual review. Audio must stay explicitly unreviewed unless listened to.

For a transformation, produce one usable scene reference first and inspect it. Keep its verified identity/wardrobe design as an input for each subsequent pose. Generate one still at a time, verify the returned file and compare source/result pairs. Repair a defective reference before advancing. Keep the exact image prompt beside each output. Add `source_frame` and `image_prompt_file` paths to its map entry; use `generated` or `edited` rather than `extracted_original`. This is a real image-tool workflow, not a change to JSON status alone. If multiple characters share the shot, inspect their appearance and scale together before using separate detail references.

Write the final, source-specific English text to `shot-prompt.txt` in the task directory. Include explicit chronological bindings such as `frame-02.png at 2 s` for the files actually selected; use their actual source timestamps. Keep identity constraints separate from expression/action. For a provider whose reference syntax is verified, also record the upload-order mapping and use its supported tags in the provider-ready version. Unresolved provider controls must remain unresolved even if the local packet passes checks.

Run `python3 scripts/check_reference_pack.py TASK_DIRECTORY`. It rejects missing/changed files, absent declared review, missing purposes, disordered times, missing prompt bindings and transformation packets without edited/generated images. A successful result means internal consistency, not proven visual fidelity. Show the images and individual files to the user. Do not declare the full motion-transfer workflow tested until an actual generated video has also been inspected.
