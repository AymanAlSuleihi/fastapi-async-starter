from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable

from src.core.events import ApplicationEvent, Event
from src.extensions.logs import get_logger

logger = get_logger(__name__)

Handler = Callable[..., Awaitable[None]]


class Hub:
    def __init__(self) -> None:
        self._subscribers: dict[type[Event], list[Handler]] = defaultdict(list)

    def subscribe(self, *event_types: type[Event]):
        def decorator(handler: Handler) -> Handler:
            for event_type in event_types:
                self._subscribers[event_type].append(handler)
            return handler

        return decorator

    async def emit(self, event: Event) -> None:
        await self._dispatch(event)

    async def track(self, event: ApplicationEvent) -> None:
        await self._dispatch(event)

    async def _dispatch(self, event: Event) -> None:
        handlers = self._subscribers.get(type(event), [])
        if not handlers:
            return

        coros = [handler(event) for handler in handlers]
        results = await asyncio.gather(*coros, return_exceptions=True)

        for handler, result in zip(handlers, results, strict=True):
            if isinstance(result, Exception):
                logger.error(
                    "event_handler_failed",
                    event_type=type(event).__name__,
                    handler=getattr(handler, "__name__", handler),
                    error=str(result),
                )


hub = Hub()
