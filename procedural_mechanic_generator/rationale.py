"""Design rationale generation."""

from __future__ import annotations

from .models import GenerationContext, MechanicBlueprint
from .utils import title_case


class DesignRationaleEngine:
    """Explains why the mechanic was constructed the way it was."""

    def analyze(self, context: GenerationContext, blueprint: MechanicBlueprint) -> dict[str, str]:
        return {
            "genre_alignment": (
                f"The mechanic honors {title_case(context.normalized_input.genre)} expectations by centering "
                f"{blueprint.core_loop[0].lower()} and then escalating with {blueprint.core_loop[-1].lower()}."
            ),
            "player_psychology": (
                "The structure alternates safety and commitment so players feel ownership over risk, "
                "learn through readable consequences, and experience mastery through increasingly intentional choices."
            ),
            "engagement_loops": (
                "Short-term loops reward execution, mid-term loops reward route or build planning, "
                "and long-term loops reward uncovering new branches that change decision texture rather than just output size."
            ),
            "why_this_mechanic_works": (
                f"It works because the resource model ({', '.join(blueprint.resources[:3])}) is directly tied to visible player actions, "
                "so every gain, setback, and escalation remains legible to players and straightforward for designers to tune."
            ),
        }
