# Standard Libraries
from typing import Iterable

# Own Libraries
from apps.map_my_world.models import Category as CategoryModel
from apps.map_my_world.models import Location as LocationModel
from apps.map_my_world.models import LocationCategory as LocationCategoryModel
from apps.utils.decorator import async_database


class QueryLocationCategoryProcess:
    """
    A class to handle querying operations for LocationCategoryModel
    objects asynchronously.

    """

    @async_database()
    def get_objects(self, **kwargs) -> list[LocationCategoryModel]:
        """
        Retrieve a list of LocationCategoryModel objects based on the
        provided filters.

        """
        return list(
            LocationCategoryModel.objects.select_related(
                "location",
                "category",
            ).filter(**kwargs)
        )

    @async_database()
    def get_object(self, **kwargs) -> LocationCategoryModel | None:
        """
        Retrieve a single LocationCategoryModel object based on the
        provided filters.

        """
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
        """
        Retrieve a dictionary mapping location IDs to sets of categories.

        Returns:
            dict[int, Iterable[LocationCategoryModel]] | None: A dictionary
            mapping location IDs to sets of LocationCategoryModel objects,
            or None if no location categories are found.
        """
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
    """
    A class to handle editing operations for LocationCategoryModel objects asynchronously.

    """

    @async_database()
    def save_instance(
        self,
        instance_to_save: LocationCategoryModel,
        update_fields: list[str] | None = None,
    ) -> LocationCategoryModel:
        """
        Save the provided LocationCategoryModel instance asynchronously.

        """
        instance_to_save.save(update_fields=update_fields)
        return instance_to_save

    @async_database()
    def bulk_create(
        self, objs: list[LocationCategoryModel]
    ) -> list[LocationCategoryModel]:
        """
        Create multiple LocationCategoryModel instances asynchronously.

        """
        return LocationCategoryModel.objects.bulk_create(objs=objs)


class LocationCategoryProcess(
    QueryLocationCategoryProcess,
    EditionLocationCategoryProcess,
):
    """
    A combined class inheriting querying and editing operations for
    LocationCategoryModel objects asynchronously.
    """

    async def create_instances(
        self,
        location: LocationModel,
        categories_list: list[CategoryModel],
    ) -> list[LocationCategoryModel]:
        """
        Create multiple LocationCategoryModel instances asynchronously.

        Args:
            location (LocationModel): The location for which to create
                LocationCategoryModel instances.
            categories_list (list[CategoryModel]): The list of categories
                to associate with the location.

        Returns:
            list[LocationCategoryModel]: A list of the created
            LocationCategoryModel instances.
        """
        instances_to_save = [
            LocationCategoryModel(
                location=location,
                category=category,
            )
            for category in categories_list
        ]

        return await self.bulk_create(objs=instances_to_save)
