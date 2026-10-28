# Interactive motion

Select by behavior: CSS for simple state transitions, Motion for React/Vue state/layout/gestures, GSAP for coordinated timelines and scroll/SVG. Prefer the project's existing compatible stack. Read the installed official `motion` skill's best-practices entry and relevant platform file; its local guidance works without MCP. Use current official docs for APIs.

Define trigger, initial state, transition, interrupt/reverse behavior and resting state. Test fast repeated activation and route changes, not just a first entrance. Preserve focus, keyboard operation, DOM semantics and reduced-motion preferences. Reduced motion should preserve the state change with less spatial movement, not hide content.

Keep animation state out of unnecessary React rerenders. Avoid forced layout in per-frame callbacks. Clean up timelines, observers and subscriptions on unmount. Do not assume filters or clipping are cheap on every device: measure relevant real interactions before claiming performance.

Verify in the browser: entrance/exit, interruption, resize, keyboard and reduced-motion state. Include the relevant mobile viewport. Check console failures and broken interactions. Report measured performance only when a trace was actually captured. MotionScore is a separate upstream capability requiring its actual connected service; a local code review is not a MotionScore audit.

Use the available Figma motion workflow only for actual Figma tasks. A Figma animation or web component is not automatically a rendered video, a Lottie export, or an After Effects project.
