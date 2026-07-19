from fastapi import APIRouter, Query, status

from src.modules.items.dependencies import ItemServiceDep, ValidItemIdDep
from src.modules.items.schemas import ItemCreate, ItemList, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=ItemList)
async def list_items(
    service: ItemServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    items, total = await service.list_items(page=page, page_size=page_size)
    return ItemList(items=[ItemRead.model_validate(i) for i in items], total=total)


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item: ValidItemIdDep):
    return item


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(data: ItemCreate, service: ItemServiceDep):
    return await service.create(data)


@router.patch("/{item_id}", response_model=ItemRead)
async def update_item(
    data: ItemUpdate,
    service: ItemServiceDep,
    item: ValidItemIdDep,
):
    return await service.update(item.id, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    service: ItemServiceDep,
    item: ValidItemIdDep,
):
    await service.delete(item.id)
