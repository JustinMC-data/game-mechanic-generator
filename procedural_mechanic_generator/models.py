"""Domain models shared across the system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class UserInput:
    """Normalized request for mechanic generation."""

    theme: str | None = None
    genre: str | None = None
    complexity: str | None = None
    mechanic_type: str | None = None
    constraints: tuple[str, ...] = ()
    demo_mode: bool = False
    debug: bool = False


@dataclass
class ErrorDetail:
    """Structured error returned to callers instead of raising."""

    code: str
    message: str
    field: str | None = None
    severity: str = "error"


@dataclass
class ValidationReport:
    """Validation results across input, logic, and output schema."""

    is_valid: bool
    errors: list[ErrorDetail] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class GenerationContext:
    """Deterministic context shared across modules."""

    normalized_input: UserInput
    seed: int
    trace_id: str


@dataclass
class MechanicBlueprint:
    """Intermediate mechanic representation before formatting."""

    mechanic_name: str
    description: str
    core_loop: list[str]
    player_actions: list[str]
    system_rules: list[str]
    resources: list[str]
    progression_hooks: list[str]
    risk_reward_structure: list[str]
    edge_cases: list[str]
    ue5_blueprint_stub: dict[str, list[str]]
    resource_state: dict[str, int | float]
    tags: list[str]
    tuning: dict[str, float]


@dataclass
class SimulationStep:
    """Single deterministic simulation step."""

    tick: int
    phase: str
    player_decision: str
    system_response: str
    resource_delta: dict[str, int | float]
    outcome: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "phase": self.phase,
            "player_decision": self.player_decision,
            "system_response": self.system_response,
            "resource_delta": self.resource_delta,
            "outcome": self.outcome,
        }


@dataclass
class GenerationResult:
    """Final result returned by the service."""

    success: bool
    output: dict[str, Any] | None = None
    errors: list[dict[str, Any]] = field(default_factory=list)
    logs: list[dict[str, Any]] = field(default_factory=list)
