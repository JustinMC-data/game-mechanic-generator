"""Output formatting and schema validation."""

from __future__ import annotations

from typing import Any

from .models import ErrorDetail, GenerationContext, MechanicBlueprint, SimulationStep, ValidationReport
from .utils import title_case


class OutputFormattingLayer:
    """Formats the final schema-compliant JSON object."""

    REQUIRED_FIELDS = {
        "mechanic_name": str,
        "theme": str,
        "genre": str,
        "complexity": str,
        "description": str,
        "core_loop": list,
        "player_actions": list,
        "system_rules": list,
        "resources": list,
        "progression_hooks": list,
        "risk_reward_structure": list,
        "simulation_output": list,
        "balancing_notes": list,
        "novelty_analysis": dict,
        "design_rationale": dict,
        "edge_cases": list,
        "ue5_blueprint_stub": dict,
        "export_version": str,
    }

    def format(
        self,
        context: GenerationContext,
        blueprint: MechanicBlueprint,
        simulation: list[SimulationStep],
        balancing_notes: list[str],
        novelty_analysis: dict[str, Any],
        rationale: dict[str, str],
    ) -> dict[str, Any]:
        return {
            "mechanic_name": blueprint.mechanic_name,
            "theme": title_case(context.normalized_input.theme),
            "genre": title_case(context.normalized_input.genre),
            "complexity": title_case(context.normalized_input.complexity),
            "description": blueprint.description,
            "core_loop": blueprint.core_loop,
            "player_actions": blueprint.player_actions,
            "system_rules": blueprint.system_rules,
            "resources": blueprint.resources,
            "progression_hooks": blueprint.progression_hooks,
            "risk_reward_structure": blueprint.risk_reward_structure,
            "simulation_output": [step.to_dict() for step in simulation],
            "balancing_notes": balancing_notes,
            "novelty_analysis": novelty_analysis,
            "design_rationale": rationale,
            "edge_cases": blueprint.edge_cases,
            "ue5_blueprint_stub": blueprint.ue5_blueprint_stub,
            "export_version": "2.0",
        }

    def validate_schema(self, payload: dict[str, Any]) -> ValidationReport:
        errors: list[ErrorDetail] = []
        for field_name, field_type in self.REQUIRED_FIELDS.items():
            if field_name not in payload:
                errors.append(ErrorDetail(code="missing_field", message=f"Missing field '{field_name}'.", field=field_name))
                continue
            if not isinstance(payload[field_name], field_type):
                errors.append(
                    ErrorDetail(
                        code="invalid_field_type",
                        message=f"Field '{field_name}' must be of type {field_type.__name__}.",
                        field=field_name,
                    )
                )

        novelty = payload.get("novelty_analysis", {})
        if isinstance(novelty, dict):
            score = novelty.get("novelty_score")
            if not isinstance(score, int) or not 0 <= score <= 100:
                errors.append(
                    ErrorDetail(
                        code="invalid_novelty_score",
                        message="novelty_score must be an integer between 0 and 100.",
                        field="novelty_analysis.novelty_score",
                    )
                )

        return ValidationReport(is_valid=not errors, errors=errors)
