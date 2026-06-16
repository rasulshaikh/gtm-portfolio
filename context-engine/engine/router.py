"""GTM Context Engine router - fuses workflows.io steps, ColdIQ skills, Rasul repos."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

ENGINE_ROOT = Path(__file__).resolve().parent.parent


def _load_json(relative: str) -> Dict[str, Any]:
    path = ENGINE_ROOT / relative
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _heat_tier(score: int, tiers: List[Dict[str, Any]]) -> Dict[str, Any]:
    sorted_tiers = sorted(tiers, key=lambda t: t["min_score"], reverse=True)
    for tier in sorted_tiers:
        if score >= tier["min_score"]:
            return tier
    return sorted_tiers[-1]


def route(
    motion_id: str,
    signal: Optional[str] = None,
    signals: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Return a context bundle for the given motion and optional signal(s)."""
    engine = _load_json("data/gtm-context-engine.json")
    skill_router = _load_json("coldiq/skill-router.json")
    plays = _load_json("coldiq/plays-index.json")

    motion = next((m for m in engine["motions"] if m["id"] == motion_id), None)
    if not motion:
        available = [m["id"] for m in engine["motions"]]
        raise ValueError(f"Unknown motion '{motion_id}'. Available: {available}")

    signal_list = list(signals or [])
    if signal and signal not in signal_list:
        signal_list.insert(0, signal)

    signal_contexts: List[Dict[str, Any]] = []
    total_score = 0
    for sig in signal_list:
        ctx = skill_router["signals"].get(sig)
        if ctx:
            entry = {"signal": sig, **ctx}
            signal_contexts.append(entry)
            total_score += ctx.get("points", 0)

    if len(signal_list) >= skill_router["compound_rules"]["min_signals_for_stack"]:
        total_score += skill_router["compound_rules"]["stack_bonus_points"]

    tier = _heat_tier(total_score, engine["heat_tiers"]) if signal_contexts else None

    primary_signal = signal_contexts[0] if signal_contexts else None
    copy_hook = primary_signal.get("copy_hook", "signal-led") if primary_signal else "billboard"

    play = None
    if primary_signal and primary_signal.get("play"):
        play = next((p for p in plays["plays"] if p["id"] == primary_signal["play"]), None)

    steps_key = "layers" if "layers" in motion else "steps"
    steps = motion.get(steps_key, [])

    bundle: Dict[str, Any] = {
        "motion": motion_id,
        "motion_title": motion["title"],
        "description": motion["description"],
        "source": motion["source"],
        "source_url": motion.get("source_url"),
        "motion_file": motion.get("motion_file"),
        "primary_repo": f"https://github.com/rasulshaikh/{motion['primary_repo']}",
        "n8n": motion.get("n8n"),
        "coldiq_skills": motion.get("coldiq_skills", []),
        "tools": motion.get("tools", []),
        "steps": steps,
        "signals": signal_list,
        "signal_contexts": signal_contexts,
        "score": total_score,
        "heat_tier": tier,
        "copy_hook": copy_hook,
        "copy_framework": f"profile/copy-framework.json#{copy_hook}",
        "gates": engine["gates"],
        "gtm_play": play,
        "agent_context": {
            "read_first": "context-engine/ENGINE.md",
            "motion_doc": f"context-engine/{motion.get('motion_file', '')}",
            "coldiq_skill": (
                primary_signal["path"]
                if primary_signal
                else skill_router["compound_rules"]["fallback_path"]
            ),
        },
        "actions": _tier_actions(tier, motion),
    }

    if motion_id == "product-signup" and "tier_routing" in motion:
        bundle["tier_routing"] = motion["tier_routing"]

    return bundle


def _tier_actions(
    tier: Optional[Dict[str, Any]], motion: Dict[str, Any]
) -> Dict[str, Any]:
    if not tier:
        return {
            "owner": "SDR",
            "sla_hours": 72,
            "channels": ["smartlead-sequence"],
            "repos": [motion["primary_repo"]],
        }
    return {
        "owner": tier["owner"],
        "sla_hours": tier.get("sla_hours"),
        "channels": tier["channels"],
        "repos": [
            motion["primary_repo"],
            "gtm-list-quality-scorecard",
            "gtm-omnibound-clay-workflow",
        ],
    }


def list_motions() -> List[Dict[str, str]]:
    engine = _load_json("data/gtm-context-engine.json")
    return [
        {"id": m["id"], "title": m["title"], "primary_repo": m["primary_repo"]}
        for m in engine["motions"]
    ]


def list_signals() -> List[str]:
    skill_router = _load_json("coldiq/skill-router.json")
    return sorted(skill_router["signals"].keys())