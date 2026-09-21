# Motion and browser-resource integration

## Choose the least machinery that serves the design
State feedback, spatial continuity, editorial emphasis and atmosphere have different needs. Establish interaction frequency, motion tolerance, rendering budget and target devices before choosing a library. Prefer CSS/native behavior for simple work. No animated hero, loader, WebGL canvas or smooth-scroll library is mandatory.

GSAP is a timeline option; Lenis is a scrolling option; React Three Fiber is a React 3D renderer; ShaderGradient/Vanta/liquid libraries and React Bits provide optional patterns. Dot Matrix is loading feedback, not a reason to invent delays. They are not interchangeable and should not all be installed together.

## Before integration
Inspect existing package manager/lockfile/framework/React versions, runtime boundaries and exact upstream ref. Read scripts and dependencies before install; approve added dependencies/network effects. Review each license (GSAP is not MIT by default). Existing approved motion must not be overwritten by repository defaults.

## Integration checklist
- One owner for each animation/render clock. When combining Lenis/GSAP/3D, check integration APIs for the installed versions; prevent duplicate requestAnimationFrame loops.
- Scope styles, listeners, observers, scroll triggers and canvas resources; clean them up on unmount/navigation. Dispose GPU textures/materials/geometries as relevant.
- Preserve anchors, focus, keyboard navigation, native scroll restoration and browser history. Never make interaction depend on hover alone.
- Respect prefers-reduced-motion. Provide static/no-WebGL fallbacks and pause unnecessary offscreen/background rendering. Test context loss when relevant.
- Check contrast over moving/transparent backgrounds, resize/orientation, content length, touch devices, layout shifts and battery/performance cost. Do not claim a CSS token alone proves legibility.
- Test the actual build and page. Playwright CLI/library/MCP require real installed tools/browser; inspect the chosen entry point. Never disable sandbox policy to obtain a test.

## Deliver
Working scoped implementation, exact versions and fallback behavior, actual test evidence, and open risks. If execution is unavailable, provide code plus NOT RUN. Save only the durable decision in the existing ACO.md.

Sources: [Design Motion Principles](https://github.com/kylezantos/design-motion-principles), [Lenis](https://github.com/darkroomengineering/lenis), [GSAP](https://github.com/greensock/GSAP), [React Three Fiber](https://github.com/pmndrs/react-three-fiber), [Playwright CLI](https://github.com/microsoft/playwright-cli). Source URLs for individual effects are in the resource registry.
