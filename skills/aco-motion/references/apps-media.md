# ACO — video applications and browser media

## Player and rendering

Use a reusable composition with typed input props as the shared visual source for preview and export. Embed the supported Remotion Player in a React app when required, with explicit dimensions, duration, fps and validated props. Other frameworks need a verified integration boundary; do not assume React components are native Vue/Svelte components.

Keep preview state, render-job state and completed-file state distinct. Check feature/codec and resource limits before selecting browser-side rendering. For server rendering, design authentication, job ownership, input validation, bounded media size/time, concurrency and cancellation before enabling real jobs. Avoid accepting arbitrary untrusted file paths or URLs for server fetches. Use idempotent requests and verify final output before showing a download link.

A cloud provider is an explicit infrastructure choice, not the default consequence of embedding a Player. Confirm deployment scope, storage/retention, service availability and cost before provisioning. Deliver a local working path when that is the user's requested scope.

## Media inspection and processing

For browser media use an installed supported library such as Mediabunny, with current API documentation. Read actual tracks, duration, dimensions, rotation and codec support; container metadata and decodable content are different checks. Handle unsupported or damaged files with a useful error rather than a fabricated duration. Release media resources and object URLs after processing.

Choose local ffprobe/ffmpeg for suitable offline inspection/transcoding when available. Work on derived outputs and preserve inputs. For browser loading verify CORS and access, without uploading private media merely to solve an implementation convenience. Large-file memory use, cancellation and progress must be tested with realistic input, not only a tiny sample.
