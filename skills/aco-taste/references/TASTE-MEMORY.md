# Taste memory and preference evidence (ACO original; Incline study)

**Goal:** make taste learnable from the project and the owner's stated reasons, without claiming that a model trained or silently extrapolating universal preferences.

1. Create a collection named for the project, deliverable or direction. A collection may hold user descriptions, images, public URLs and design-guide notes; images remain local and identified by digest. No quiz is mandatory; supplied references are already evidence.
2. Mark each reference `inspiration`, `direction`, `negative` or `constraint`. A `direction` is not authorization to copy an entire design. Write *what exactly* should be kept or avoided (scale, crop, density, rhythm, transitions) and record scope.
3. For iterative work, record significant change/checkpoint, concrete artifact path, explicit user's reaction, and cause. Choices `prefer`, `reject`, `both`, `neither`, `depends`, `revision`, `approve` are **relative and scope-limited**.
4. Synthesize insights by aspect and retrieve linked evidence before applying. A single `prefer` does not become permanent style policy. The same author may prefer opposing things for different projects.
5. Maintain project-local state (`.aco-taste/collections.json`, `.aco-taste/feedback.jsonl`) separate from ACO's private `ACO_HOME` and code root. The shared/personal library is opt-in, not discovered/modified automatically.
6. Historical evidence is append-only by default. Bad JSON is an error, not permission to reset a collection or overwrite the journal. Ask before importing personal collections into another client context.
7. Treat the user's *negative* examples as first-class evidence; record what fails and why. Never convert silence into satisfaction.

CLI: `taste.py collection-new`, `reference-add`, `feedback-add`, `insights`, `status`. This implementation is deliberately local and stdlib-based. It does not claim the upstream Incline visual-session UI, browser token login, or cross-project synchronization.
