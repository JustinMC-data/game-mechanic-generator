"""Utility helpers for deterministic generation."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import UserInput


def canonicalize(value: str | None) -> str | None:
    """Normalize string inputs while preserving semantic content."""
    if value is None:
        return None
    normalized = " ".join(value.strip().lower().split())
    return normalized or None


def canonical_constraints(values: list[str] | tuple[str, ...] | None) -> tuple[str, ...]:
    """Normalize constraints as a stable, sorted tuple."""
    if not values:
        return ()
    normalized = sorted({canonicalize(value) for value in values if canonicalize(value)})
    return tuple(normalized)


def make_seed(user_input: UserInput) -> int:
    """Create a deterministic seed from normalized input."""
    payload = json.dumps(
        {
            "theme": user_input.theme,
            "genre": user_input.genre,
            "complexity": user_input.complexity,
            "mechanic_type": user_input.mechanic_type,
            "constraints": list(user_input.constraints),
            "demo_mode": user_input.demo_mode,
        },
        sort_keys=True,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def stable_trace_id(seed: int) -> str:
    """Short deterministic trace identifier for logs."""
    return f"mech-{seed:016x}"[:17]


def bounded(value: float, lower: float, upper: float) -> float:
    """Clamp a value to an allowed range."""
    return max(lower, min(upper, value))


def title_case(value: str | None) -> str:
    """User-facing capitalization helper."""
    if not value:
        return ""
    return " ".join(part.capitalize() for part in value.split())


def hash_pick(options: list[Any], seed: int, offset: int = 0) -> Any:
    """Select a deterministic item without importing random."""
    if not options:
        raise ValueError("options must not be empty")
    index = (seed + offset) % len(options)
    return options[index]
