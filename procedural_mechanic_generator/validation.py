"""Cross-module validation and feasibility checks."""

from __future__ import annotations

from .config import CONTRADICTION_RULES
from .models import ErrorDetail, GenerationContext, ValidationReport


class ValidationLayer:
    """Validates contradictions, feasibility, and numeric safety."""

    def validate_context(self, context: GenerationContext) -> ValidationReport:
        errors: list[ErrorDetail] = []
        constraints = set(context.normalized_input.constraints)

        for rule in CONTRADICTION_RULES:
            if rule["constraints"].issubset(constraints):
                errors.append(
                    ErrorDetail(code="contradictory_constraints", message=rule["message"], field="constraints")
                )

        if context.normalized_input.genre == "survival" and context.normalized_input.mechanic_type == "economy":
            errors.append(
                ErrorDetail(
                    code="feasibility_warning",
                    message="Economy-heavy survival mechanics are supported but may require additional scarcity tuning.",
                    field="genre",
                    severity="warning",
                )
            )

        hard_errors = [error for error in errors if error.severity == "error"]
        return ValidationReport(is_valid=not hard_errors, errors=hard_errors, warnings=[e.message for e in errors if e.severity == "warning"])
