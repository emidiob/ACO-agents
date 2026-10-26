# Fictional worked cases

These illustrate ACO brief-to-prompt decisions. They are not provider tests, upload receipts or observations of a user's media. Replace labels with verified interface references only when supported.

## Preserve a source clip

Brief: a continuous six-second shot shows a gloved technician setting a glass prism into a padded tray. Retain every visual property. Bind `source_clip` to motion and appearance; source frames establish the beginning, hand contact and ending. Exact event times come from source inspection.

Draft:

```text
Use the supplied clip as the reference for both appearance and movement. Reproduce the technician lowering the glass prism into the padded tray, preserving the original hand positions, viewing angle and action pace. The prism remains supported until it rests in the tray; the hand then releases it as in the source. Keep the same gloves, bench layout, reflections and camera behavior. Finish at the source's final composition, with the prism resting in its original position. Retain the source audio only through a supported audio workflow.
```

No replacement-character images are required. Settings remain unresolved until a provider is selected.

## Change the performer

Brief: transfer a seated drummer's performance to a user-designed robot. `source_clip` governs motion and camera; `robot_design` governs appearance. Contact anchors must establish how the robot's hands hold the sticks. If robot anatomy cannot perform the source pose, resolve that design issue before promising a faithful transfer.

Draft:

```text
Transfer the seated performance from the supplied clip to the robot shown in the design reference. Preserve the performer's position and occupied space, the order of the stick strikes and the original camera framing. Use the robot reference for body design and materials only. The contact anchors define the stick grips and arm orientation. Keep the robot seated throughout, with the instrument layout unchanged. Match the visible performance timing; the separate audio plan governs sound.
```

If the required contact anchors have not been made, label this a draft and list the missing references.

## Animate one photograph

Brief: a close image of a ceramic cup; steam begins to rise while the frame holds.

```text
Keep the cup, tabletop and composition from the supplied photograph. Thin steam rises from the liquid, curls briefly above the rim and disperses into the surrounding air. The cup stays still. Hold the camera position and preserve the existing soft side light and ceramic texture. No speech or music.
```

Choose still-to-video only if supported. A reference photo does not imply any observed motion.

## Continue across a boundary

Brief: extend a source ending with a cyclist moving left to right. Inspect the source tail before drafting.

```text
Continue from the supplied ending without resetting the cyclist's pose or position. Maintain the existing direction and speed while the cyclist travels toward the right edge of the frame. Carry the camera movement, illumination and background motion across the boundary. End with the cyclist leaving the frame, if the available duration permits that motion naturally.
```

Verify extension inputs and supported duration; do not imply a working extension feature from this text alone.

## Repair a contact error

Evidence: the generated handle separates from the hand briefly, while the rest of the shot is acceptable. Identify the actual interval and inspect its neighboring frames. First propose an interval edit preserving grip and timing. Do not rewrite the scene or delete the interval without checking synchronization requirements.
