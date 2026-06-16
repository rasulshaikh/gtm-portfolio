#!/usr/bin/env python3
"""CLI for GTM Context Engine routing."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from router import list_motions, list_signals, route  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="GTM Context Engine router")
    parser.add_argument("--motion", help="Motion id: signal-activation, gtm-flywheel, product-signup, outbound-attribution")
    parser.add_argument("--signal", help="Single signal type")
    parser.add_argument("--signals", help="Comma-separated signals for compound scoring")
    parser.add_argument("--list", action="store_true", help="List available motions")
    parser.add_argument("--list-signals", action="store_true", help="List signal types")
    parser.add_argument("--json", action="store_true", help="Output JSON bundle")
    args = parser.parse_args()

    if args.list:
        for m in list_motions():
            print(f"  {m['id']:20} {m['title']} -> {m['primary_repo']}")
        return 0

    if args.list_signals:
        for s in list_signals():
            print(f"  {s}")
        return 0

    if not args.motion:
        parser.error("--motion is required (or use --list)")

    sigs = None
    if args.signals:
        sigs = [s.strip() for s in args.signals.split(",") if s.strip()]

    try:
        bundle = route(args.motion, signal=args.signal, signals=sigs)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(bundle, indent=2))
        return 0

    print(f"Motion:     {bundle['motion_title']}")
    print(f"Repo:       {bundle['primary_repo']}")
    if bundle["signals"]:
        print(f"Signals:    {', '.join(bundle['signals'])}")
        print(f"Score:      {bundle['score']}")
        if bundle["heat_tier"]:
            print(f"Heat:       {bundle['heat_tier']['id']} (SLA {bundle['heat_tier'].get('sla_hours')}h)")
    print(f"Copy hook:  {bundle['copy_hook']}")
    print(f"ColdIQ:     {bundle['agent_context']['coldiq_skill']}")
    print(f"Read:       {bundle['agent_context']['read_first']}")
    print()
    print("Steps:")
    for step in bundle["steps"]:
        n = step.get("order", "?")
        impl = step.get("implementation", "")
        print(f"  {n}. {step['name']} -> {impl}")
    print()
    print("Gates:")
    for g in bundle["gates"]:
        print(f"  - {g['id']}: {g['repo']} ({g['threshold']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())