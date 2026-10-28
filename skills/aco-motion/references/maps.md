# ACO — geographic motion

Choose the least complex technique that supports the shot: a licensed static map with vector overlays for a simple route; MapLibre/Mapbox/MapTiler for interactive styles and camera moves; a terrain/globe engine such as Cesium for real 3D geography. Library availability does not include tile rights, a terrain service, credits or credentials. Do not equate an open-source map renderer with free access to every data source.

Validate real coordinates, longitude/latitude order, route sequence and attribution requirements. Record projection and bounds. For routes crossing the antimeridian, unwrap longitude or split geometry deliberately; naive interpolation can travel around the wrong side of the globe. Prefer supplied verified geography over guessed place positions.

For a static image determine its geographic bounds before projecting overlays; uncalibrated pixels cannot produce accurate coordinates. For a live map drive camera and route progress from the video frame clock. Wait for style, tiles, fonts and idle/load state before capture, with a bounded timeout and visible failure. Disable autonomous easing when deterministic video frames are required.

Project labels and pins through the active camera rather than mixing geographic and pixel coordinates. Verify start/end locations, intermediate path, occlusion and label readability in the final export. Keep attribution visible where required. Test random seeks and rendering without an interactive browser session. If remote data cannot be reproduced, prepare an authorized cached/static asset or report the dependency; do not silently substitute invented geography.
