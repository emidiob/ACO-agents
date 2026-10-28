# ACO — captions and sound

## Timed text

Inspect supplied SRT/VTT/JSON before choosing transcription. Keep original text and time units identifiable. If transcription is needed, discover an actual authorized local tool or service; never fabricate words or word timings. Store an editable caption representation with text, start/end in milliseconds and optional confidence, preserving uncertainty. Use the installed caption package's types when integrating with Remotion.

Reject nonfinite, negative or reversed intervals. Sort cues and inspect overlaps; overlap may be intentional, so resolve by content rather than blindly deleting it. Convert composition frame time to milliseconds once. Account for media trim, playback speed and sequence offset when mapping source caption time into the final timeline.

Group words into readable lines and pages according to speech and available space. If only sentence timing exists, do not call interpolated word highlights measured alignment. Check long words, punctuation, line breaks, multilingual shaping and safe areas in the final aspect ratio. Inspect the first cue, page transitions and last cue in playback. Keep editable subtitle data or a requested sidecar with the source.

## Sound design

Use real licensed audio and source durations. A generator is an optional actual capability, not an assumed voice API. Place voice first when it carries meaning, then music and purposeful effects. Tie an effect to an observed motion event; do not add a whoosh to every cut by default. Back-time music against its real ending only after listening and inspecting its rhythm. Do not pretend a generated beat grid is verified by ear.

Automate volume in timeline time; use short fades at cuts to avoid clicks. Verify gain summation, clipping, true peak/loudness against the intended destination where specified. Listen to the export, not only isolated assets. If listening is unavailable, state that sync/mix quality remains unverified even when metadata and meters pass. Preserve stems or a music-free variant when requested, without expanding every small task into a full audio package.
