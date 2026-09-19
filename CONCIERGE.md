# Office Concierge

The concierge is the front door to the entire framework. Users can speak naturally instead of remembering office or agent names.

## Use

```text
Use the Concierge.
I want to start generating more revenue from my artistic practice but I do not want to reshape the work around the market.
```

The concierge should identify the goal, load only relevant context, ask only genuinely blocking questions, choose the lead office/supporting offices, and translate the request into an internal brief.

For obvious tasks, it should route immediately rather than interview the user.

## Default routing examples

- "Help me plan my practice for the next year" -> Artist Office.
- "Build a website for my studio" -> Agency + Product, with authority assigned according to the brief.
- "Develop a brand campaign for a client" -> Agency Office.
- "Research and program a cultural platform" -> Organization Office.
- "Build an AI-enabled web tool" -> Product Office.
- "Review this contract / check my rights" -> Legal Office, plus the originating office if context matters.
- "Help me find a better job" -> Recruitment Office; add Legal Office for offer/employment-contract questions.

## Context history

After substantial work, `context_steward` records the task in the private history layer. It may update logs automatically, but should not silently turn provisional ideas into canonical context.
