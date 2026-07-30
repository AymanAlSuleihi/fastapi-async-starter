from src.extensions.hub import hub
from src.extensions.logs import get_logger
from src.modules.items.events import ItemCreated, ItemDeleted

logger = get_logger(__name__)


@hub.subscribe(ItemCreated)
async def log_item_created(event: ItemCreated) -> None:
    logger.info("item_created", item_id=event.item_id, name=event.name)


@hub.subscribe(ItemDeleted)
async def log_item_deleted(event: ItemDeleted) -> None:
    logger.info("item_deleted", item_id=event.item_id, name=event.name)
