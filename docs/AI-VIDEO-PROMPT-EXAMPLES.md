# Original AI-video prompt examples

These are ACO-authored **creative drafts**, not tested renders or universal API payloads. Resolve the exact model/interface, authorized input references and supported duration/settings before use. For image-to-video, the input image should establish appearance; text focuses on motion. Desired-action wording is useful for the documented Runway Gen-4 guidance, but do not assume every provider handles controls identically.

## 1. Product detail reveal — image-to-video
**Direction:** one restrained reveal, not several edits inside a clip.

> The folded edge slowly lifts, revealing the paper seam beneath it. The camera makes a short, steady move forward at the object's height. The movement settles as the seam becomes clearly visible.

**Check:** edge geometry, input-object identity, camera drift and the final hold. Put generation duration, aspect ratio and source reference in the real provider fields.

## 2. Small performance beat — image-to-video
**Direction:** attention changes before a large physical action.

> The person pauses while listening, shifts their gaze toward the doorway, then lets their shoulders relax. The camera holds a steady medium close-up. Their expression settles into quiet recognition.

**Check:** eye direction, face consistency, excessive expression changes and unwanted camera movement.

## 3. Walking coverage — text-to-video or verified reference mode
**Direction:** establish a legible screen direction for the following cut.

> A person in a plain coat walks from left to right through a simple interior corridor. The camera tracks alongside at a consistent distance and waist height. The pace is measured, with the person still moving toward the right edge at the end.

**Check:** body/wardrobe identity, foot motion and whether the next shot preserves the intended direction.

## 4. Intentional material transformation — experimental work
**Direction:** one controlled impossible event rather than accidental inconsistency.

> The smooth clay surface gradually opens into a field of shallow folds. The transformation travels from the center toward the edges while the object remains in place. A fixed overhead camera holds the entire change in view.

**Check:** distinguish the intended transformation from unrelated morphing; preserve the artist's concept rather than forcing physical realism.

## 5. Reaction insert for an edit
**Direction:** a readable reaction that can connect two existing shots.

> The hand stops just above the envelope, hesitates briefly, then rests beside it. The camera stays close and still. The shot ends on the hand and envelope held in that quiet arrangement.

**Check:** prop position and hand placement against the previous/next shots; preserve enough edit handles.

## 6. Loop-oriented motion
**Direction:** return toward a comparable state; not a guarantee of a seamless loop.

> The suspended sheet makes a small, slow sway to one side and back toward its starting position. The camera remains fixed, and the movement keeps a gentle, even rhythm.

**Check:** inspect start/end alignment and velocity. A compositing/editing solution may be needed for a clean seam; the prompt alone cannot guarantee it.

## From a film idea to prompts
First define the scene's purpose, beats and essential coverage. Assign shot IDs; build a timing/continuity table; choose the actual generation mode and model per shot. Draft and test a small authorized sample. Inspect full clips and the edit. Save prompts, settings, references and real receipts. A montage is usually assembled from separate shots; do not blindly request all cuts, dialogue, effects and transformations in one overloaded prompt.

Primary reading: [Runway Gen-4 prompting](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide), [Google video prompting](https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide). No source prompt examples were copied.
