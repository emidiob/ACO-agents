# Media resources

Optional catalogue, not an installation list. Consult current source and actual host capabilities.

## open-higgsfield

**Open Higgsfield AI** · unresolved · identity_unresolved · reviewed 2026-09-20

Source: Unresolved; exact link required.

**Use:** Resolve which similarly named project is intended before proposing a deployment.

**Avoid:** Do not claim it is official Higgsfield, locally rendered, free, private or already integrated.

**Checks:** Multiple candidates exist; some use hosted model APIs and public asset URLs. Exact repo, privacy and cost review required.

Roles: `generative_media_director`, `security_reviewer`.

Required capabilities when executing: none declared; inspect the actual task/tool.

[Original ACO method](../playbooks/MEDIA-RESOURCE-METHOD.md). External upstream content is not bundled. No execution tests performed.

Unconfirmed candidates: https://github.com/Anil-matcha/Open-Higgsfield-AI, https://github.com/wide-trace/open-higgsfield. Obtain the exact intended source; do not auto-select.

## voicebox

**Voicebox** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/jamiepine/voicebox

**Use:** Optional local audio/voice production and transcription through a separately configured app/MCP.

**Avoid:** Voice synthesis/transcription does not place phone calls; never clone a real voice without appropriate permission.

**Checks:** Verify app, model licenses, consent, MCP endpoint auth and whether any selected backend sends audio remotely.

Roles: `sound_designer`, `podcast_audio_producer`, `communications_operator`.

Required capabilities when executing: local_execution, voice_consent.

[Original ACO method](../playbooks/MEDIA-RESOURCE-METHOD.md). External upstream content is not bundled. No execution tests performed.

## open-llm-vtuber

**Open-LLM-VTuber** · runtime · source_reviewed · reviewed 2026-09-20

Source: https://github.com/Open-LLM-VTuber/Open-LLM-VTuber

**Use:** Explore an explicitly requested interactive voice/avatar installation or interface.

**Avoid:** Not a necessary office dependency, a phone service, or evidence that every model runs privately offline.

**Checks:** Check model/voice/avatar licenses, consent, microphone/storage boundaries and selected provider routes.

Roles: `creative_technologist`, `sound_designer`, `ai_product_engineer`.

Required capabilities when executing: local_execution, voice_consent.

[Original ACO method](../playbooks/MEDIA-RESOURCE-METHOD.md). External upstream content is not bundled. No execution tests performed.

## hyperframes

**HyperFrames** · framework · source_reviewed · reviewed 2026-09-20

Source: https://github.com/heygen-com/hyperframes

**Use:** Evaluate programmatic video composition as an optional rendering route.

**Avoid:** Do not conflate deterministic composition with generated live-action footage or install alongside Remotion unnecessarily.

**Checks:** Review exact runtime, license, fonts/assets, rendering dependencies and output verification. Not execution-tested here.

Roles: `remotion_video_engineer`, `motion_designer`, `media_pipeline_engineer`.

Required capabilities when executing: local_execution.

[Original ACO method](../playbooks/MEDIA-RESOURCE-METHOD.md). External upstream content is not bundled. No execution tests performed.

## comfyui-continuity

**ComfyUI Continuity** · comfyui_node · source_reviewed · reviewed 2026-09-20

Source: https://github.com/roadmaus/ComfyUI-Continuity

**Use:** Plan reference roles, still pre-stage, shots and family-specific local rendering through the optional node.

**Avoid:** No perfect continuity or six audio/video families promise. Avoid duplicate old/new packs; do not auto-delete old folders or download weights.

**Checks:** Current README: two video/audio families and four still families; optional prompt refiner can call a remote API. Audit core/nodes/GPU/models/licenses, cache/drift and data routes.

Roles: `comfyui_workflow_engineer`, `visual_prompt_engineer`, `script_continuity_supervisor`, `generative_video_qc`.

Required capabilities when executing: local_execution, comfyui, gpu_models.

[Original ACO method](../playbooks/MEDIA-RESOURCE-METHOD.md). External upstream content is not bundled. No execution tests performed.

## gallery-dl

**gallery-dl** · cli · source_reviewed · reviewed 2026-09-20

Source: https://github.com/mikf/gallery-dl

**Use:** Acquire authorized public/owned gallery media and metadata for research, archival or production workflows.

**Avoid:** Do not bypass access controls, download material without rights/permission, or treat site support as permission under platform terms or copyright.

**Checks:** External CLI; GPLv2. Record source URL, rights basis, date and metadata when material enters an archive.

Roles: `media_data_wrangler`, `practice_archivist`, `artwork_documentation_manager`, `content_researcher`.

Required capabilities when executing: local_execution.

[Original ACO method](../playbooks/FILE-TRANSFER-ARCHIVE.md). External upstream content is not bundled. No execution tests performed.

## cobalt

**Cobalt** · application · source_reviewed · reviewed 2026-09-20

Source: https://github.com/imputnet/cobalt

**Use:** Save authorized publicly accessible media for research/reference when source rights and platform terms allow it.

**Avoid:** Do not use to evade paywalls/access controls, remove attribution obligations or download copyrighted material without a lawful basis.

**Checks:** External downloader. Repository licensing is mixed by component (AGPL core; web terms differ); ACO bundles none of it.

Roles: `media_data_wrangler`, `content_researcher`, `visual_researcher`.

Required capabilities when executing: external_or_local_app.

[Original ACO method](../playbooks/FILE-TRANSFER-ARCHIVE.md). External upstream content is not bundled. No execution tests performed.
