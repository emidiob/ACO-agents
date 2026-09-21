# Editorial, image and finishing interoperability

Original ACO operational method · v0.6.0. Select for the relevant task; do not load every playbook.

## Before touching media
Verify source files, edit intent, frame rates/timebases, color information, audio layout, destination specifications, storage and reversible output paths. Metadata may be incomplete; ask rather than guessing camera transforms. Never overwrite the only original or bake an irreversible transform into a master without approval.

## Select the smallest tool
Use the installed production application or a narrow local tool for the task. FFmpeg can inspect/transcode/mux/filter, but build features and codec availability vary. OpenTimelineIO represents editorial timing and references; it does not embed all source media or guarantee every effect survives interchange. OpenImageIO can inspect/process image data; it is not a substitute for a human retouch review. Match the operation to the actual installed version.

## Round-trip evidence
For timeline interchange, compare clip count, source references, in/out ranges, gaps, transitions, timebase and audio offsets after importing into the receiving application. For image processing, compare dimensions, channels, alpha handling, bit depth, color metadata and visual appearance. Preserve originals and a dependency manifest when the task requires reproducibility.

Check representative frames and audio after export, then final duration, sync, loudness specifications when supplied, clipping, levels, subtitles and delivery packaging. A successful command or identical filename is not evidence of correct content. Avoid claiming broadcast compliance or a calibrated display when not verified.

## Practical execution
Prefer argument arrays and local files over constructed shell strings. Bound external execution with an authorized purpose, cost/storage estimate and an output path. Do not install codecs, custom nodes or binaries implicitly. A plan may specify a command with placeholders, but must be labeled unexecuted when no media/tool is available.

## Delivery and record
Return the actual output, checks performed and unresolved issues. Keep the important recipe and canonical master reference with the production project; do not upload temporary proxy, probe log or each test frame as permanent Drive memory. Logs supporting a commissioned QC deliverable remain artifacts rather than mandatory memory objects.

## References and use boundary
The linked sources inform scope and factual tool selection. Their courses, software, skill bundles and protected text are not included or relicensed by ACO. Recheck current terms before external reuse.

- [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html)
- [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO)
- [OpenImageIO](https://github.com/AcademySoftwareFoundation/OpenImageIO)
