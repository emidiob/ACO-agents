# ACO — preview and export

## Preview

Use the existing package manager and local CLI. Once the project can run, start Studio, read the actual URL emitted and open that URL with an available browser tool. Reuse the project's running server when suitable. Check that the intended composition loads with its real assets; a listening port is insufficient. Keep the preview available during visual iterations.

## Render

An explicit export request authorizes the needed local render. Establish composition ID, props, dimensions, fps, duration, codec and destination. Run the installed CLI's help to confirm flags for that version. The ordinary operations are `remotion compositions`, `remotion still`, and `remotion render`, invoked through the local package manager; do not let an absent local CLI trigger an unreviewed latest-package download.

First render representative frames for costly scenes: opening, active movement, landing, transition boundaries and last frame. Render the full requested file after fixing visible faults. Use a new destination or verified user-owned output; avoid overwriting source media. Preserve failed-render diagnostics and reconcile output state before retrying.

## Format decisions

For a normal MP4 use a compatible video/audio combination and destination-supported pixel format. For alpha, choose a codec/container that actually supports transparency; an MP4 file does not prove alpha support. Check the installed renderer's supported ProRes/WebM options, pixel format and transparency settings rather than guessing flags. Test the exported alpha over contrasting backgrounds.

Inspect the actual output's duration, resolution, fps, audio streams and file size with available metadata tools. Watch meaningful sections and transitions; listen when audio matters. A contact sheet verifies only sampled appearance. Record actual checks and residual limitations, then return the file, source and reproducible composition/settings. Cloud rendering, deployments and paid APIs remain separate scoped actions.
