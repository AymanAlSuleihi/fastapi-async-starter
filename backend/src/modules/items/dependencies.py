import uuid
from typing import Annotated

from fastapi import Depends, Path

from src.db.engine import DbDep
from src.modules.items.models import Item
from src.modules.items.service import ItemService


async def get_item_service(db: DbDep) -> ItemService:
    return ItemService(db)


ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]


async def valid_item_id(
    item_id: Annotated[uuid.UUID, Path(description="The ID of the item")],
    db: DbDep,
) -> Item:
    return await ItemService(db).get_by_id(item_id)


ValidItemIdDep = Annotated[Item, Depends(valid_item_id)]
