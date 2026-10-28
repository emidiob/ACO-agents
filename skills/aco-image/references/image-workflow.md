# Image execution

1. Resolve output dimensions/aspect, intended use and the few invariants that affect the result. Do not turn a simple request into a questionnaire.
2. Inspect available references. Use `scripts/reference_inventory.py` to record immutable file hashes when handing a set to another tool or person. Its output is metadata only: it cannot approve appearance.
3. Build a specific prompt from observed content and requested changes. Keep API settings separate. Verify current input, masking and output capabilities before binding references; use only real returned upload IDs.
4. Run the requested creation/edit with the host image tool. Preserve its returned output file and actual settings. If execution fails, report the error and retry only when the cause can be corrected within scope.
5. Open the output and compare identity, requested edit, layout, material/light, exact text and unchanged regions where relevant. Fix the concrete defect rather than appending generic quality adjectives. Report unverified details and deliver the actual image.

A reference inventory, prompt, tool receipt and reviewed image are four different artifacts. Do not label an inventory or a successful tool call as visual acceptance. Image generation uses external engines; the ACO contribution is the method and preparation/review workflow.
