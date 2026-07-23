import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.items.exceptions import ItemNotFound
from src.modules.items.models import Item
from src.modules.items.schemas import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_items(self, page: int = 1, page_size: int = 20) -> tuple[list[Item], int]:
        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(Item).offset(offset).limit(page_size).order_by(Item.created_at.desc())
        )
        items = list(result.scalars().all())
        total = await self.db.scalar(select(func.count(Item.id)))
        return items, total or 0

    async def get_by_id(self, item_id: uuid.UUID) -> Item:
        item = await self.db.scalar(select(Item).where(Item.id == item_id))
        if not item:
            raise ItemNotFound(str(item_id))
        return item

    async def create(self, data: ItemCreate) -> Item:
        item = Item(**data.model_dump())
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, item_id: uuid.UUID, data: ItemUpdate) -> Item:
        item = await self.get_by_id(item_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete(self, item_id: uuid.UUID) -> None:
        item = await self.get_by_id(item_id)
        await self.db.delete(item)
        await self.db.commit()
