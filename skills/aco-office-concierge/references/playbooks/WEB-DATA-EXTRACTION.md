# Web data extraction and browser automation

Choose the lightest authorized method that works.

1. Prefer direct official APIs or normal page fetch/search when sufficient.
2. Use structured crawlers/scrapers for repeatable extraction; browser automation only when interaction/dynamic state requires it.
3. Define fields, pages, sampling/QC, rate limit, robots/terms and authentication before a large run.
4. Never evade access controls, CAPTCHAs or site restrictions.
5. Treat extracted data as observations with provenance, not automatically verified facts.
6. For private/logged-in pages, explicitly approve credentials/data destination and keep secrets out of scripts/logs.
7. Verify a small sample before scaling.
