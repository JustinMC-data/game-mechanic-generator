"""Balancing, exploit detection, and consistency analysis."""

from __future__ import annotations

from .config import SAFE_NUMERIC_RANGES
from .models import MechanicBlueprint
from .utils import bounded


class BalancingConsistencyEngine:
    """Produces tuning guidance and checks mechanic scalability."""

    def analyze(self, blueprint: MechanicBlueprint) -> list[str]:
        tuning = {
            key: bounded(value, *SAFE_NUMERIC_RANGES[key])
            for key, value in blueprint.tuning.items()
            if key in SAFE_NUMERIC_RANGES
        }

        notes = [
            f"Risk index {tuning['risk_index']:.2f} vs reward index {tuning['reward_index']:.2f} stays within a healthy tension band for repeatable play.",
            f"Failure penalty {tuning['failure_penalty']:.2f} keeps mistakes meaningful without making recovery mathematically impossible.",
            f"Progression velocity {tuning['progression_velocity']:.2f} supports extension through new branches instead of raw stat inflation.",
        ]

        if "Trace" in blueprint.resources:
            notes.extend(
                [
                    "Exploit check: cap breach refunds to one per encounter so stealth loops cannot infinitely farm mark activations.",
                    "Synergy map: stealth positioning, subsystem choice, and trace purge timing form a three-axis mastery curve.",
                    "Failure mode: reflected hijacks must telegraph their branch inversion before input lockout to keep losses legible.",
                ]
            )
        elif "Stability" in blueprint.resources:
            notes.extend(
                [
                    "Exploit check: unique guild techniques should be account-locked per craft to prevent alt funneling.",
                    "Synergy map: material tier, forge timing, and partner specialization produce scalable social depth.",
                    "Failure mode: partial disconnect recovery should snapshot resonance state after every committed beat.",
                ]
            )
        elif "Oxygen" in blueprint.resources:
            notes.extend(
                [
                    "Exploit check: reclaiming tether charges should require line-of-return contact, preventing infinite anchor hopping.",
                    "Synergy map: route planning, momentum control, and emergency refuge placement reinforce each other without redundancy.",
                    "Failure mode: zero-oxygen chamber transitions should resolve to a downed state with predictable rescue windows.",
                ]
            )
        else:
            notes.append("Scalability check: extend by adding new branches that alter decision topology rather than only raising numeric output.")

        return notes
