# ComfyUI and generative pipeline protocol

Read official current ComfyUI docs and the actual authorized environment before building a graph. UI workflow JSON and API prompt JSON differ. Record ComfyUI version/commit, Python/PyTorch/CUDA or platform, GPU/VRAM, model identifiers/licenses, custom-node repositories/revisions and input/output paths. Never invent a class_type or assume a model filename exists.

Use the instance's verified node schema (for example authorized GET /object_info) and system/model inventory when available. Do not expose the instance publicly or collect secrets in the public repo. If environment access is absent, request a workflow export and relevant metadata, or produce a clearly labeled blueprint.

Start with a minimal pilot. Static validation checks shape, node availability, required inputs and links. Actual server validation, memory use, image quality and temporal consistency require an authorized run. A /prompt queue response is not a completed render; reconcile by returned job/prompt ID and inspect actual output.

Unknown nodes/packages require review, source/license checks, version pinning and installation authorization. Do not upgrade a working production environment implicitly. Use safe copies/branches or a separate environment for experiments. Never install arbitrary code to make an unknown workflow “just work.”

For training, use consented/authorized data, a held-out evaluation set, model/data versioning and explicit compute limits. Prompt/model/output provenance belongs in the private project. Document nondeterminism and rejection criteria.

The bundled comfy-preflight helper accepts API prompt JSON and an object_info JSON snapshot. It performs limited static checks only, never contacts a server, installs nodes, downloads models or queues work. It does not validate dynamic node behavior or visual results.
