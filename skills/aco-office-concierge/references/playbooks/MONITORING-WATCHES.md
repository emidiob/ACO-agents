# Monitoring and watches

Monitoring is a deployed capability, not a promise from a prompt.

1. Define exactly what is watched, why, how often and what counts as a meaningful change/failure.
2. Choose availability monitoring for service health; page-change monitoring for content changes. Do not confuse them.
3. Respect robots.txt, terms, access policy, rate limits and authentication boundaries.
4. Route alerts to an authorized destination and define deduplication/maintenance windows.
5. Test one failure/change and verify the alert path before calling monitoring active.
6. Store only the watch definition/status in ACO; do not create a project/file per observed event.
