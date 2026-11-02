#!/usr/bin/env python3
"""ACO Taste Deepening: assess directions, contextual feedback and review receipts."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from aco_taste import deepening


def _packet(path):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("Packet must be a JSON object")
    return obj


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="action", required=True)
    for name in ("variants", "cycle", "motion"):
        sub = subs.add_parser(name)
        sub.add_argument("--packet", required=True)
    fb = subs.add_parser("feedback")
    fb.add_argument("--project", required=True)
    fb.add_argument("--query", required=True)
    fb.add_argument("--scope", default="current-project")
    fb.add_argument("--aspect")
    fb.add_argument("--limit", type=int, default=5)
    args = parser.parse_args(argv)
    try:
        if args.action == "variants":
            output = deepening.evaluate_variants(_packet(args.packet))
        elif args.action == "cycle":
            output = deepening.check_review_cycle(_packet(args.packet))
        elif args.action == "motion":
            output = deepening.motion_triage(_packet(args.packet))
        else:
            output = deepening.query_feedback(args.project, args.query, scope=args.scope,
                                              aspect=args.aspect, limit=args.limit)
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
