# Production resources

Optional catalogue, not an installation list. Consult current source and actual host capabilities.

## ffmpeg

**FFmpeg** · tool · source_reviewed · reviewed 2026-09-20

Source: https://ffmpeg.org/ffmpeg.html

**Use:** Probe sources, perform authorized media processing and verify output against delivery specifications.

**Avoid:** Inspect installed build, filters, encoders and applicable licenses. Preserve originals and verify timebase, color, audio, subtitles and duration.

**Checks:** Inspect installed build, filters, encoders and applicable licenses. Preserve originals and verify timebase, color, audio, subtitles and duration.

Roles: `video_editor`, `media_pipeline_engineer`, `media_delivery_qc`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/MEDIA-INTERCHANGE.md). External upstream content is not bundled. No execution tests performed.

## opentimelineio

**OpenTimelineIO** · library · source_reviewed · reviewed 2026-09-20

Source: https://github.com/AcademySoftwareFoundation/OpenTimelineIO

**Use:** Exchange editorial timeline structure and validate round trips.

**Avoid:** Timeline metadata is not embedded media or a guarantee that every effect, speed change, transition or color transform survives.

**Checks:** Timeline metadata is not embedded media or a guarantee that every effect, speed change, transition or color transform survives.

Roles: `online_editor_conform`, `video_editor`, `media_pipeline_engineer`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/MEDIA-INTERCHANGE.md). External upstream content is not bundled. No execution tests performed.

## openimageio

**OpenImageIO** · tool · source_reviewed · reviewed 2026-09-20

Source: https://github.com/AcademySoftwareFoundation/OpenImageIO

**Use:** Inspect and process image sequences with explicit channels, metadata and color assumptions.

**Avoid:** Pixel transforms require actual color context. Command success does not approve a retouch or a grade.

**Checks:** Pixel transforms require actual color context. Command success does not approve a retouch or a grade.

Roles: `media_pipeline_engineer`, `color_pipeline_engineer`, `photo_retouch_artist`.

Required capabilities when executing: current_tool_or_connector_review.

[Original ACO method](../playbooks/MEDIA-INTERCHANGE.md). External upstream content is not bundled. No execution tests performed.
