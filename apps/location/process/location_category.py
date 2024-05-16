# Standard Libraries
from typing import Iterable

# Own Libraries
from apps.map_my_world.models import Category as CategoryModel
from apps.map_my_world.models import Location as LocationModel
from apps.map_my_world.models import LocationCategory as LocationCategoryModel
from apps.utils.decorator import async_database


class QueryLocationCategoryProcess:
    @async_database()
    def get_objects(self, **kwargs):
        return list(
            LocationCategoryModel.objects.select_related(
                "location",
                "category",
            ).filter(**kwargs)
        )

    @async_database()
    def get_object(self, **kwargs) -> LocationCategoryModel | None:
        return (
            LocationCategoryModel.objects.select_related(
                "location",
                "category",
            )
            .filter(**kwargs)
            .first()
        )

    async def get_categories_index_dict(
        self,
    ) -> dict[int, Iterable[LocationCategoryModel]] | None:
        if location_categories := await self.get_objects(
            is_deleted=False,
        ):
            location_id_list = {loc_cat.location_id for loc_cat in location_categories}
            return {
                location_id: {
                    location_cat.category
                    for location_cat in location_categories
                    if location_cat.location_id == location_id
                }
                for location_id in location_id_list
            }


class EditionLocationCategoryProcess:

    @async_database()
    def save_instance(
        self,
        instance_to_save: LocationCategoryModel,
        update_fields: list[str] | None = None,
    ) -> LocationCategoryModel:
        instance_to_save.save(update_fields=update_fields)
        return instance_to_save

    @async_database()
    def bulk_create(
        self, objs: list[LocationCategoryModel]
    ) -> list[LocationCategoryModel]:
        return LocationCategoryModel.objects.bulk_create(objs=objs)


class LocationCategoryProcess(
    QueryLocationCategoryProcess,
    EditionLocationCategoryProcess,
):

    async def create_instances(
        self,
        location: LocationModel,
        categories_list: list[CategoryModel],
    ) -> list[LocationCategoryModel]:

        instances_to_save = [
            LocationCategoryModel(
                location=location,
                category=category,
            )
            for category in categories_list
        ]

        return await self.bulk_create(objs=instances_to_save)
