from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class AuditEvent:
    event_type: str
    object_type: str
    object_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class AuditService:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record_event(
        self,
        *,
        event_type: str,
        object_type: str,
        object_id: str,
    ) -> AuditEvent:
        event = AuditEvent(
            event_type=event_type,
            object_type=object_type,
            object_id=object_id,
        )
        self._events.append(event)
        return event

    def list_events(self, object_id: str) -> list[AuditEvent]:
        return [event for event in self._events if event.object_id == object_id]
