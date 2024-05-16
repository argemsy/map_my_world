# Standard Libraries
import logging
from datetime import datetime, timezone

# Own Libraries
from apps.location.process.location_category import LocationCategoryProcess

logger = logging.getLogger(__name__)


async def register_views(location_id: int, category_id: int):
    """
    Asynchronous function for registering views for a location in a
    specific category.

    Args:
        location_id (int): The ID of the location.
        category_id (int): The ID of the category.
    """

    log_tag = "register_views"
    logger.debug(f"***BACKGROUND TASK: {log_tag}***")

    process = LocationCategoryProcess()

    if instance := await process.get_object(
        location_id=location_id,
        category_id=category_id,
        is_deleted=False,
    ):

        instance.total_reviews += 1
        instance.updated_at = datetime.now(timezone.utc)

        await process.save_instance(
            instance_to_save=instance,
            update_fields=[
                "updated_at",
                "total_reviews",
            ],
        )
