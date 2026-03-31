"""Genre-aware novelty analysis."""

from __future__ import annotations

from .config import GENRE_CONVENTIONS
from .models import GenerationContext, MechanicBlueprint


class NoveltyAnalysisEngine:
    """Compares the generated mechanic against genre conventions."""

    def analyze(self, context: GenerationContext, blueprint: MechanicBlueprint) -> dict[str, object]:
        conventions = GENRE_CONVENTIONS.get(context.normalized_input.genre, {})
        baseline = set(conventions.get("novel_baseline", []))
        tags = set(blueprint.tags)
        divergence = len(tags - baseline)
        overlap = len(tags & baseline)
        score = max(35, min(94, 58 + divergence * 9 - overlap * 3 + len(context.normalized_input.constraints) * 2))

        explanation = (
            f"The mechanic keeps expected {context.normalized_input.genre} structure through "
            f"{', '.join(conventions.get('expected_loops', ['recognizable genre loops']))}, "
            f"but becomes more novel by combining {', '.join(blueprint.tags[:3])}. "
            f"It avoids direct convention overlap in {max(0, divergence)} major areas while still remaining implementable."
        )
        return {"novelty_score": score, "explanation": explanation}
