# ACO — motion review and repair

Review the artifact against the supplied brief and actual reference. Identify timestamp or interaction, observed failure, probable cause, smallest repair and verification needed. Prioritize wrong content, broken actions, unreadability and temporal discontinuity before cosmetic polish.

## Video checks

Check scene ordering, readable landings, object continuity, unexpected freezes, flashes, clipping, late-loading assets, font substitution, end-frame behavior and audio sync. Compare source/target samples at the same meaningful event, not arbitrary equal timestamps after a retime. A contact sheet is useful for composition but cannot certify smoothness. Measure durations and audio levels when relevant; listen/watch before claiming those qualities. Fix the highest-impact defects and rerender the affected range before a final export.

## UI checks

Exercise entrance, exit, interrupted transition, repeated rapid activation, resize, navigation and cleanup. Test keyboard/focus, screen-reader semantic state and reduced-motion mode. Reduced motion must still show the outcome; shorten/remove spatial motion without hiding necessary content. Check mobile layout and touch behavior when applicable.

Use browser performance traces for actual performance claims. Inspect long tasks, repeated layout/paint, expensive filters, main-thread work and excess compositor layers. Transform/opacity are useful starting points but not a universal guarantee of acceleration. Scope any will-change hint and remove it when no longer useful. Never fabricate FPS, device results or a trace.

## Review evidence and stopping

Separate observed facts from hypotheses. After a repair rerun the failing case and one relevant regression; stop when acceptance conditions are met rather than adding endless speculative changes. Use an independent reviewer only when authorized and materially useful; do not claim one ran if it did not. An ACO review is not the proprietary MotionScore service. Report local observations and measurements without using its grading system or reconstructing gated methodology.
