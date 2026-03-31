"""Static configuration used by the mechanic generator."""

from __future__ import annotations

ALLOWED_THEMES = {
    "cyberpunk",
    "fantasy",
    "high fantasy",
    "cosmic horror",
    "space horror",
    "post-apocalypse",
    "mythic sci-fi",
    "dieselpunk",
}

ALLOWED_GENRES = {
    "roguelike",
    "mmo",
    "deck-builder",
    "survival",
    "immersive sim",
    "rts",
    "action rpg",
}

ALLOWED_COMPLEXITIES = {"simple", "medium", "advanced"}

ALLOWED_MECHANIC_TYPES = {"combat", "crafting", "traversal", "economy", "ai behavior"}

SAFE_NUMERIC_RANGES = {
    "risk_index": (0.0, 1.0),
    "reward_index": (0.0, 1.0),
    "failure_penalty": (0.0, 10.0),
    "progression_velocity": (0.1, 5.0),
}

GENRE_CONVENTIONS = {
    "roguelike": {
        "expected_loops": ["run-based escalation", "resource scarcity", "adaptation under uncertainty"],
        "novel_baseline": ["proc-gen encounters", "meta progression", "high failure tolerance"],
    },
    "mmo": {
        "expected_loops": ["social coordination", "long-term progression", "crafting specialization"],
        "novel_baseline": ["guild economies", "tiered crafting", "repeatable encounters"],
    },
    "survival": {
        "expected_loops": ["resource pressure", "environmental mastery", "sustained attrition"],
        "novel_baseline": ["hunger or oxygen pressure", "shelter planning", "hazard routing"],
    },
    "deck-builder": {
        "expected_loops": ["synergy assembly", "tempo decisions", "draft adaptation"],
        "novel_baseline": ["card cycling", "archetype pivots", "resource sequencing"],
    },
}

CONTRADICTION_RULES = [
    {
        "constraints": {"low gravity", "fall damage multiplier 3x"},
        "message": "Low gravity conflicts with an extreme fall-damage multiplier unless an explicit counter-force system exists.",
    },
    {
        "constraints": {"no magic", "mana economy"},
        "message": "The 'no magic' constraint conflicts with mana-based mechanics.",
    },
    {
        "constraints": {"permadeath", "persistent squad revival"},
        "message": "Permadeath conflicts with persistent revival unless revival is externalized to future runs.",
    },
]

DEMO_PROFILE = {
    "theme": "mythic sci-fi",
    "genre": "immersive sim",
    "complexity": "advanced",
    "mechanic_type": "combat",
    "constraints": ["asymmetric time dilation", "diegetic UI", "energy debt"],
}
