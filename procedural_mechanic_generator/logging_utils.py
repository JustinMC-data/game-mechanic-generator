"""Internal structured logging helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class EventLogger:
    """Captures structured generation events for debug and monitoring."""

    trace_id: str
    debug: bool = False
    events: list[dict[str, Any]] = field(default_factory=list)

    def log(self, stage: str, message: str, **details: Any) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trace_id": self.trace_id,
            "stage": stage,
            "message": message,
            "details": details,
        }
        if self.debug or stage in {"input", "validation_error", "output"}:
            self.events.append(event)

    def dump(self) -> list[dict[str, Any]]:
        return list(self.events)
