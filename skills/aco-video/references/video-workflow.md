# Video execution

For a new shot, establish initial state, observable action and end state. For multiple shots record duration, transition and continuity per shot. Build only the storyboard detail the job requires; a one-shot request does not need a sequence of invented cuts.

Inspect actual anchor images. Record their filenames and influence; use `scripts/reference_inventory.py` for a handoff manifest when needed. Missing references remain missing, never synthetic upload tags. A text description of a desired anchor is not a delivered anchor. Create requested reference images through an available image tool and inspect them before video execution.

Before rendering, verify provider/model/interface, input limits, duration, aspect, resolution and audio support from the actual interface or current official documentation. Keep unsupported values as production targets. The method works without provider selection; a provider-ready prompt requires verified bindings and settings. Seedance-specific examples do not establish support in another engine.

If generation is requested and authorized, submit through the available tool, retain its receipt and reconcile an unknown outcome before retrying. Return actual generated media, not a fabricated download link. If the tool is missing, deliver prepared references, the shot-specific prompt and unresolved settings.

Review actual playback for timing, contacts, occlusion, identity, camera continuity and cuts. Listen to audio before assessing it. Sample frames can support a visual review but do not prove continuous motion or sound. Compare output with requested start/end states; repair the smallest affected interval when supported. Retain unreviewed fields explicitly. ACO prepares and directs; an external video engine produces pixels.
