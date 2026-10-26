# Visual evidence and anchors

Start with duration, dimensions, frame rate and stream presence. Audio-stream metadata says nothing about what is heard. Variable-frame-rate files require timestamps rather than assuming every frame has equal duration.

Sample the whole clip, then inspect more closely where the action changes, subjects overlap, hands contact objects, direction reverses or a cut may occur. Report the sampling scope. Dense frame strips or playback are needed for subtle timing; a sparse contact sheet is insufficient to claim frame-exact choreography.

For each meaningful event record the observed state before, the transition and the state after. Mark uncertainty explicitly. When exact cut timing matters, compare adjacent frames at the candidate boundary. Automated scene scores are suggestions and can miss cuts or flag lighting changes.

## Anchor selection

Choose frames that constrain different failure risks:

- Opening and final composition establish the spatial path.
- Contact frames establish support, grip and which surface occludes another.
- Turning frames establish orientation and which features are visible.
- An overlap frame establishes subject count and relative depth.

Keep source timestamp, extraction method and image dimensions with each anchor. Use enough anchors to remove ambiguity, within the provider's input budget; more images are not automatically better. Do not fabricate an intermediate action to fill a sampling gap.

For unchanged recreation, extract and deliver the original frames as separate usable files; a contact sheet alone is not the reference package. For a requested transformation, inspect generated/edited anchor images before using them: the intended change must be consistent while pose, scale and layout remain appropriate. Do not represent a proposed preview as a finished file. Never add hidden subjects merely because a character reference shows them.

## Reference conflicts

Resolve conflicts explicitly: a face reference may have different illumination, a wardrobe image may show a different pose, and a material photo may contain an irrelevant room. Assign influence per attribute. If equally authoritative references disagree, ask the one decisive choice rather than averaging incompatible designs.

Local extraction produces analysis artifacts only. Leave the source untouched and save output outside the library, using a new destination. The supplied helper refuses an existing destination to prevent accidental overwrite.

## Delivery check

Before calling references ready, open the image outputs, verify their files exist and match the intended source moments, show the user the set, and provide individual download links. Follow [reference delivery](reference-delivery.md). Do not confuse a frame specification with an extracted or generated image.
