"""Input normalization and request pre-validation."""

from __future__ import annotations

from .config import (
    ALLOWED_COMPLEXITIES,
    ALLOWED_GENRES,
    ALLOWED_MECHANIC_TYPES,
    ALLOWED_THEMES,
    CONTRADICTION_RULES,
    DEMO_PROFILE,
)
from .logging_utils import EventLogger
from .models import ErrorDetail, UserInput, ValidationReport
from .utils import canonical_constraints, canonicalize


class InputLayer:
    """Normalizes raw user input and catches early contradictions."""

    def normalize(self, payload: dict, logger: EventLogger) -> tuple[UserInput, ValidationReport]:
        if payload is None or not isinstance(payload, dict):
            malformed = ValidationReport(
                is_valid=False,
                errors=[ErrorDetail(code="malformed_input", message="Input payload must be a JSON object.", field=None)],
            )
            return UserInput(), malformed

        demo_mode = bool(payload.get("demo_mode", False))
        if demo_mode:
            normalized = UserInput(
                theme=DEMO_PROFILE["theme"],
                genre=DEMO_PROFILE["genre"],
                complexity=DEMO_PROFILE["complexity"],
                mechanic_type=DEMO_PROFILE["mechanic_type"],
                constraints=tuple(DEMO_PROFILE["constraints"]),
                demo_mode=True,
                debug=bool(payload.get("debug", False)),
            )
            logger.log("input", "Demo mode enabled; substituted demo profile.", normalized=normalized.__dict__)
            return normalized, ValidationReport(is_valid=True)

        normalized = UserInput(
            theme=canonicalize(payload.get("theme")),
            genre=canonicalize(payload.get("genre")),
            complexity=canonicalize(payload.get("complexity")),
            mechanic_type=canonicalize(payload.get("mechanic_type")),
            constraints=canonical_constraints(payload.get("constraints")),
            demo_mode=False,
            debug=bool(payload.get("debug", False)),
        )

        errors: list[ErrorDetail] = []

        if not normalized.theme:
            errors.append(ErrorDetail(code="missing_theme", message="Theme is required unless demo_mode is true.", field="theme"))
        elif normalized.theme not in ALLOWED_THEMES:
            errors.append(
                ErrorDetail(code="invalid_theme", message=f"Unsupported theme '{payload.get('theme')}'.", field="theme")
            )

        if not normalized.genre:
            errors.append(ErrorDetail(code="missing_genre", message="Genre is required unless demo_mode is true.", field="genre"))
        elif normalized.genre not in ALLOWED_GENRES:
            errors.append(
                ErrorDetail(code="invalid_genre", message=f"Unsupported genre '{payload.get('genre')}'.", field="genre")
            )

        if not normalized.complexity:
            errors.append(
                ErrorDetail(code="missing_complexity", message="Complexity is required unless demo_mode is true.", field="complexity")
            )
        elif normalized.complexity not in ALLOWED_COMPLEXITIES:
            errors.append(
                ErrorDetail(
                    code="invalid_complexity",
                    message=f"Unsupported complexity '{payload.get('complexity')}'. Expected one of {sorted(ALLOWED_COMPLEXITIES)}.",
                    field="complexity",
                )
            )

        if not normalized.mechanic_type:
            errors.append(
                ErrorDetail(
                    code="missing_mechanic_type",
                    message="mechanic_type is required unless demo_mode is true.",
                    field="mechanic_type",
                )
            )
        elif normalized.mechanic_type not in ALLOWED_MECHANIC_TYPES:
            errors.append(
                ErrorDetail(
                    code="invalid_mechanic_type",
                    message=f"Unsupported mechanic type '{payload.get('mechanic_type')}'.",
                    field="mechanic_type",
                )
            )

        for rule in CONTRADICTION_RULES:
            if rule["constraints"].issubset(set(normalized.constraints)):
                errors.append(ErrorDetail(code="contradictory_constraints", message=rule["message"], field="constraints"))

        logger.log("input", "Normalized user input.", normalized=normalized.__dict__)
        report = ValidationReport(is_valid=not errors, errors=errors)
        return normalized, report
