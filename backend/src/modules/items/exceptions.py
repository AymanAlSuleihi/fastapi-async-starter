from src.core.exceptions import NotFoundException


class ItemNotFound(NotFoundException):
    def __init__(self, item_id: str | None = None):
        detail = f"Item with id {item_id} not found" if item_id else "Item not found"
        super().__init__(detail=detail, code="ITEM_NOT_FOUND")
