# ACO — web and UI animation

## Select by behavior

Keep the existing compatible stack. Use CSS transitions for simple class-driven changes, Motion for interruptible state/layout/gesture work, and GSAP for coordinated timelines, SVG or complex scroll behavior. A full video render uses [composition](composition.md), not these free-running browser mechanisms.

Define trigger, initial/rest state, duration or spring behavior, interruption/reversal and keyboard equivalent. Motion should explain a state or support the visual brief. Avoid universal bounce, hover-scale or stagger recipes. Treat timing as contextual: frequently repeated utility actions must not wait for decorative sequences.

## Framework implementation

For React identify the installed package/version before choosing `motion/react` versus a legacy integration. Keep hooks and interaction state in client components. Use presence handling for exit transitions, stable keys for identity, and layout/shared-layout mechanisms for relationships that survive DOM movement. Preserve focus restoration and semantic state when animation delays removal.

Drive high-frequency animation through motion values or the library's animation clock rather than per-frame React state. Compose derived values, clean up subscriptions, and avoid competing CSS and JavaScript owners of the same property. Animate the source of a derived value rather than attempting to animate its computed result independently.

For Vue use the installed supported Vue binding and its reactivity semantics. For vanilla JS scope element selection, retain cancel/cleanup handles and test removal/navigation. With Base UI or Radix preserve their accessibility and portal contracts: use the documented render/as-child mechanism for the installed version, control mount lifetime when exit animation needs it, and test focus and dismissal. Do not paste React patterns into Vue or assume every primitive accepts the same props.

## Scroll, SVG and springs

Choose viewport-triggered entrances versus continuous scroll progress deliberately. Preserve native anchors, keyboard scrolling and restoration. Recompute bounds when layout/media changes and tear down observers on navigation. A GSAP context/timeline must be reverted or disposed through its actual API; never add a second animation clock accidentally.

For SVG keep a valid viewBox, transform origin and geometric interpolation. Path drawing and shape morphing are different problems; normalize path compatibility or use a verified library. Preserve meaning when stroke or motion is suppressed.

Use a spring when interruption and velocity continuity matter. Use a duration/easing curve when an exact schedule matters. A browser-native CSS spring approximation can be authored locally and visually compared without a paid service; do not call it Motion's generated spring output. Prefer a supported easing fallback over unsupported syntax on target browsers.

Finish with [motion review](review.md). Library choice is not proof of accessibility or frame performance.
