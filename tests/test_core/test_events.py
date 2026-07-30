from src.core.events import ApplicationEvent, Event


class TestEvent:
    def test_event_has_id_and_timestamp(self):
        e = Event()
        assert isinstance(e.event_id, str)
        assert len(e.event_id) > 0
        assert e.timestamp is not None

    def test_event_id_is_unique(self):
        e1 = Event()
        e2 = Event()
        assert e1.event_id != e2.event_id

    def test_event_is_dataclass(self):
        from datetime import UTC, datetime

        d = {"event_id": "custom", "timestamp": datetime.now(UTC)}
        e = Event(**d)
        assert e.event_id == "custom"


class TestApplicationEvent:
    def test_is_subclass_of_event(self):
        assert issubclass(ApplicationEvent, Event)

    def test_inherits_fields(self):
        e = ApplicationEvent()
        assert isinstance(e.event_id, str)
        assert e.timestamp is not None
