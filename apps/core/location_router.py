# Standard Libraries
import logging

# Third-party Libraries
from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse

# Own Libraries
from apps.location.bg_tasks.register_location_view import register_views
from apps.location.process import LocationProcess
from apps.location.process.category import CategoryProcess
from apps.location.process.city import CityProcess
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
from apps.utils.tags import MetadataTag

logger = logging.getLogger(__name__)

location_router = APIRouter()


recommend_locations_tag = MetadataTag(
    name="Recommend Locations",
    description=(
        """This function recommends locations based on the provided category
        ID and recent total reviews. It retrieves locations that belong to the
        specified category and have been updated within the last 30 days.
        Recommendations are sorted based on the total number of reviews received
        in the past 30 days. The function returns a payload containing metadata
        about the total count of recommended locations and a list of recommended
        locations, including their IDs, names, cities, countries, and categories.
        """
    ),
)


@location_router.get(
    "/recommend-locations",
    status_code=status.HTTP_200_OK,
    tags=[recommend_locations_tag.name],
)
async def recommend_locations(category_id: int) -> LocationListPayload:
    log_tag = "Recommend Locations"
    logger.debug(f"***{log_tag}***")
    process = LocationProcess()
    category_process = LocationCategoryProcess()
    city_process = CityProcess()

    if not (
        locations := await process.recommend_locations(
            category_process=category_process,
            city_process=city_process,
            category_id=category_id,
        )
    ):
        return LocationListPayload.empty_state()

    return LocationListPayload(
        metadata=LocationMetadata(total_count=len(locations)),
        items=locations,
    )


location_detail_tag = MetadataTag(
    name="Location Detail",
    description=(
        """This resource retrieves details of a location based on its ID and category.
        It checks if the location exists and belongs to the specified category.
        If found, it retrieves additional details such as city and categories.
        It also adds a background task to register views for the location.
        If the location is not found, it returns a 404 NOT FOUND response.
        """
    ),
)


@location_router.get(
    "/location-{location_id}/category-{category_id}",
    status_code=status.HTTP_200_OK,
    tags=[location_detail_tag.name],
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
        city_process = CityProcess()
        category_process = LocationCategoryProcess()
        categories_index_dict = await category_process.get_categories_index_dict()

        bg_tasks.add_task(register_views, location_id, category_id)
        city_tuple_dict = await city_process.get_city_and_country()

        return LocationType.from_db_model(
            instance=location,
            category_id=category_id,
            city_tuple=city_tuple_dict.get(location.city_id),
            categories_list=categories_index_dict.get(location.id),
        )

    return JSONResponse(
        content={},
        status_code=status.HTTP_404_NOT_FOUND,
    )


add_location_tag = MetadataTag(
    name="Add Location",
    description=(
        """This function adds a new location with the provided input data.
        It first retrieves the categories associated with the location.
        If the categories are not found, it raises an AssertionError.
        Otherwise, it creates a new location instance and associates it
        with the retrieved categories.
        It returns a payload containing the created location and a success message.
        """
    ),
)


@location_router.post(
    "/add-locations",
    status_code=status.HTTP_201_CREATED,
    tags=[add_location_tag.name],
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
