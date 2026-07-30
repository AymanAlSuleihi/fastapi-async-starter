from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(kw_only=True)
class Event:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(kw_only=True)
class ApplicationEvent(Event):
    pass
