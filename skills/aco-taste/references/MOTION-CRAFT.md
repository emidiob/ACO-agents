# Motion craft (ACO original; Emil Kowalski skills studied)

Treat motion as a communication decision, not default polish. Record the event, why it moves, what changes, how often it is seen, its origin, duration, easing, support for interruption, and reduced-motion alternative.

- **Frequency:** repetitive keyboard commands/tables/rapid filters should favor immediate response; rare transitions may have a storytelling moment.
- **Timing:** controls normally respond promptly (~120–300ms where appropriate); cinematic title/video choreography follows the story instead of UI component timings. Do not apply web UI easing rules to a video shot.
- **Spatial continuity:** a dialog should feel tied to its trigger unless centering is intentional; entering/exiting states need deliberate asymmetry. Avoid `transition: all` and layout properties when transform/opacity can serve the same meaning.
- **Performance:** inspect actual frames and input response; avoid blur/filter abuse and permanent `will-change`. A clean source file is not measured 60fps.
- **Access:** keyboard, focus, interruptibility and `prefers-reduced-motion` must survive; animations should never hide content with JavaScript disabled.
- **Motion removal:** deleting motion can be the right design choice when it delays repeated work or produces discomfort.

Use `taste.py audit-css` for bounded static checks, and actual rendered/playback review for conclusions. Existing `aco-motion` remains the execution specialist; `aco-taste` reviews direction and result.
