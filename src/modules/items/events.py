from dataclasses import dataclass

from src.core.events import Event


@dataclass(kw_only=True)
class ItemCreated(Event):
    item_id: str
    name: str


@dataclass(kw_only=True)
class ItemDeleted(Event):
    item_id: str
    name: str
