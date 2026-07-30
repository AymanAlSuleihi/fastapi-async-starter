from src.core.events import ApplicationEvent, Event
from src.extensions.hub import Hub


class TestHub:
    async def test_subscribe_and_emit(self):
        hub = Hub()
        called_with = []

        @hub.subscribe(Event)
        async def handler(event):
            called_with.append(event.event_id)

        e = Event()
        await hub.emit(e)
        assert len(called_with) == 1
        assert called_with[0] == e.event_id

    async def test_multiple_subscribers(self):
        hub = Hub()
        results = []

        @hub.subscribe(Event)
        async def first(event):
            results.append("first")

        @hub.subscribe(Event)
        async def second(event):
            results.append("second")

        await hub.emit(Event())
        assert results == ["first", "second"]

    async def test_subscriber_for_specific_type_only(self):
        hub = Hub()
        results = []

        from dataclasses import dataclass

        @dataclass(kw_only=True)
        class SpecificEvent(Event):
            pass

        @hub.subscribe(SpecificEvent)
        async def handler(event):
            results.append("matched")

        await hub.emit(Event())  # base type — no match
        assert results == []

        await hub.emit(SpecificEvent())  # specific type — match
        assert results == ["matched"]

    async def test_track_calls_subscribers(self):
        hub = Hub()
        results = []

        @hub.subscribe(ApplicationEvent)
        async def handler(event):
            results.append("tracked")

        await hub.track(ApplicationEvent())
        assert results == ["tracked"]

    async def test_failing_subscriber_does_not_block_others(self):
        hub = Hub()
        results = []

        @hub.subscribe(Event)
        async def bad_handler(event):
            raise RuntimeError("boom")

        @hub.subscribe(Event)
        async def good_handler(event):
            results.append("ok")

        await hub.emit(Event())  # should not raise
        assert results == ["ok"]

    async def test_no_subscribers_does_nothing(self):
        hub = Hub()
        await hub.emit(Event())  # should not raise
