# Web architecture, CMS and performance

## Start from the actual project
Read package versions, build commands, hosting constraints, content ownership and existing architecture. Choose the smallest solution that meets the task: a static site does not automatically need an application framework, database, authentication or a deployment provider.

## Implementation procedure
1. Identify page types, content sources, permissions, localization, preview needs and update frequency. Sketch the data boundaries and failure modes before choosing a CMS or API.
2. Model content semantically: title, authorship, media/alt/caption/credit, publication dates, slugs and relationships. Keep presentation decisions out of durable content when avoidable. Plan redirects and exportability.
3. Define server/client boundaries appropriate to installed framework versions. Prevent cross-user cached data or shared mutable request state. Authenticate privileged actions at the server boundary.
4. Parallelize only independent data fetching. Remove avoidable waterfalls; constrain payloads and expensive dependencies. Measure first, then make one testable change.
5. Use semantic reusable components. For custom motion/3D, define a no-motion or low-resource fallback, loading budget and input model. Scroll effects must not prevent content access or keyboard navigation.
6. Define loading, error, offline/empty and timeout behaviour. Validate inputs, handle canceled requests and avoid hydration hacks that hide state mismatches.
7. Build and test under the real commands. Review dependencies and licensing separately; do not auto-install a downloaded skill's runtime or execute untrusted setup scripts.
8. Document deployment and rollback as separate authorized steps. A local preview is not a published site.

## Output
Architecture decision note, component/content model, implemented code, measured bottlenecks, tests and explicit deployment status. Refer to current official framework documentation rather than freezing an upstream skill's old API examples.

## Research provenance and limits

Comparison references: [S11](https://github.com/vercel-labs/agent-skills), [S15](https://github.com/openai/plugins), [S05](https://github.com/VoltAgent/awesome-claude-code-subagents), [S02](https://github.com/obra/superpowers).
This is an ACO-authored operating procedure, not a bundled upstream skill. No external installer, runtime, prompt collection, palette/font dataset or model weights are included. Read the source inventory for inspection scope and licence cautions. Source popularity is not a quality benchmark.
