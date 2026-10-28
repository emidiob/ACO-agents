# Validate a source checkout

Run these commands from the repository root:

```bash
python3 scripts/publication_check.py
python3 scripts/generate.py --check
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests -v
```

After intentional canonical changes, regenerate derived files with `python3 scripts/generate.py` and rebuild fingerprints with `python3 scripts/build_manifest.py` before validation.

The checks verify package consistency, documented contracts, routing behavior, source hashes and relative links. Unit tests do not establish visual quality, provider access, legal accuracy or production performance. Validate actual outputs and integrations in the target environment. Keep execution logs and internal evaluation reports outside the public source tree.

The publication check rejects known internal-document paths. It supplements editorial review; it does not detect every possible disclosure. Public packages retain executable regression fixtures and required licensing information.
