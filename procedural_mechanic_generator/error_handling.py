"""Structured error formatting helpers."""

from __future__ import annotations

from .models import ErrorDetail


class ErrorHandlingLayer:
    """Converts internal errors to stable response payloads."""

    def format_errors(self, errors: list[ErrorDetail]) -> list[dict[str, str | None]]:
        return [
            {
                "code": error.code,
                "message": error.message,
                "field": error.field,
                "severity": error.severity,
            }
            for error in errors
        ]
