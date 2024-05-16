# Standard Libraries
import logging

# Third-party Libraries
from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse

# Own Libraries
from apps.location.bg_tasks.register_location_view import register_views
from apps.location.process import LocationProcess
from apps.location.process.category import CategoryProcess
from apps.location.process.location_category import LocationCategoryProcess
from apps.location.schema.inputs.location import LocationAddInput
from apps.location.schema.response.interface import Response
from apps.location.schema.response.location import (
    CreateLocationPayload,
    LocationListPayload,
    LocationMetadata,
)
from apps.location.schema.types.location import LocationType
from apps.utils.decorator import handler_exception

logger = logging.getLogger(__name__)

location_router = APIRouter()


@location_router.get(
    "/recommend-locations",
    status_code=status.HTTP_200_OK,
)
async def recommend_locations(category_id: int) -> LocationListPayload:
    log_tag = "Recommend Locations"
    logger.debug(f"***{log_tag}***")
    process = LocationProcess()
    category_process = LocationCategoryProcess()

    if not (
        locations := await process.recommend_locations(
            category_process=category_process,
            category_id=category_id,
        )
    ):
        return LocationListPayload.empty_state()

    return LocationListPayload(
        metadata=LocationMetadata(total_count=len(locations)),
        items=locations,
    )


@location_router.get(
    "/location-{location_id}/category-{category_id}",
    status_code=status.HTTP_200_OK,
)
async def location_detail(
    location_id: int, category_id: int, bg_tasks: BackgroundTasks
) -> LocationType | None:
    log_tag = "Location detail"
    logger.debug(f"***{log_tag}***")
    process = LocationProcess()
    kwargs = {
        "is_deleted": False,
        "id": location_id,
        "locations_categories_set__category_id": category_id,
    }

    if location := await process.get_object(**kwargs):

        category_process = LocationCategoryProcess()
        categories_index_dict = await category_process.get_categories_index_dict()

        bg_tasks.add_task(register_views, location_id, category_id)

        return LocationType.from_db_model(
            instance=location,
            category_id=category_id,
            categories_list=categories_index_dict.get(location.id),
        )

    return JSONResponse(
        content={},
        status_code=status.HTTP_404_NOT_FOUND,
    )


@location_router.post(
    "/add-locations",
    status_code=status.HTTP_201_CREATED,
)
@handler_exception(payload_class=CreateLocationPayload, log_tag="Add Location")
async def add_location(input: LocationAddInput) -> CreateLocationPayload:

    location_process = LocationProcess()
    category_process = CategoryProcess()
    location_category_process = LocationCategoryProcess()

    if not (
        categories_list := await category_process.get_objects(
            id__in=input.category_id_list,
            is_deleted=False,
        )
    ):
        raise AssertionError(
            f"Categories with ID's {input.category_id_list}, not found."
        )

    new_location = await location_process.create_instance(
        input=input,
        categories_list=categories_list,
        location_category_process=location_category_process,
    )

    return CreateLocationPayload(
        location=LocationType.from_db_model(
            instance=new_location,
            category_id=input.category_id_list[0],
            categories_list=categories_list,
        ),
        response=Response(
            status_code=status.HTTP_201_CREATED,
            type="Success",
            message="",
        ),
    )
