# Standard Libraries
from datetime import datetime, timedelta, timezone

# Third-party Libraries
from django.db import DatabaseError, IntegrityError, transaction
from django.db.models import F, QuerySet

# Own Libraries
from apps.location.process.location_category import LocationCategoryProcess
from apps.location.schema.inputs.location import LocationAddInput
from apps.location.schema.types.location import LocationType
from apps.map_my_world.models import Category as CategoryModel
from apps.map_my_world.models import Location as LocationModel
from apps.utils.decorator import async_database


class QueryLocationProcess:

    @staticmethod
    def _annotate_total_reviews(
        queryset: QuerySet[LocationModel],
    ) -> QuerySet[LocationModel]:
        return queryset.annotate(
            total_reviews=F("locations_categories_set__total_reviews"),
        )

    @async_database()
    def get_objects(
        self,
        limit: int | None = 10,
        offset: int | None = 0,
        order_by: list[str] = None,
        **kwargs,
    ) -> list[LocationModel]:

        queryset = LocationModel.objects.prefetch_related(
            "locations_categories_set"
        ).filter(**kwargs)

        queryset = self._annotate_total_reviews(queryset=queryset)

        if order_by := order_by or ["-id"]:
            queryset = queryset.order_by(*order_by)

        queryset = queryset[offset : offset + limit]

        return list(queryset)

    @async_database()
    def get_object(self, **kwargs) -> LocationModel | None:
        queryset = LocationModel.objects.filter(**kwargs)
        queryset = self._annotate_total_reviews(queryset=queryset)
        return queryset.first()


class EditionLocationProcess:

    @async_database()
    def save_instance(
        self,
        instance_to_save: LocationModel,
        update_fields: list[str] | None = None,
    ) -> LocationModel:
        try:
            with transaction.atomic():
                instance_to_save.save(update_fields=update_fields)
            return instance_to_save
        except (DatabaseError, IntegrityError) as exp:
            raise DatabaseError(repr(exp)) from exp


class LocationProcess(
    QueryLocationProcess,
    EditionLocationProcess,
):

    async def recommend_locations(
        self,
        category_process: LocationCategoryProcess,
        category_id: int,
    ) -> list[LocationType | None]:

        utc_now = datetime.now(timezone.utc)
        month_before = utc_now - timedelta(days=30)

        kwargs = {
            "is_deleted": False,
            "locations_categories_set__category_id": category_id,
            "locations_categories_set__updated_at__range": [month_before, utc_now],
        }

        if locations := await self.get_objects(
            order_by=["locations_categories_set__total_reviews"],
            **kwargs,
        ):
            categories_index_dict = await category_process.get_categories_index_dict()
            return [
                LocationType.from_db_model(
                    instance=location,
                    category_id=category_id,
                    categories_list=categories_index_dict.get(location.id),
                )
                for location in locations
            ]
        return []

    async def create_instance(
        self,
        input: LocationAddInput,
        categories_list: list[CategoryModel],
        location_category_process: LocationCategoryProcess,
    ) -> LocationModel:
        try:
            location_kwargs = input.location.model_dump()
            filter_kwargs = location_kwargs.copy()
            filter_kwargs.pop("address")

            if previous_register := await self.get_object(**filter_kwargs):
                raise AssertionError(
                    f"This location {previous_register} alredy registered"
                )

            pre_saved_location = LocationModel(**location_kwargs)
            location = await self.save_instance(instance_to_save=pre_saved_location)

            await location_category_process.create_instances(
                location=location,
                categories_list=categories_list,
            )
            return location
        except AssertionError as exp:
            raise AssertionError(str(exp)) from exp
        except DatabaseError as exp:
            raise DatabaseError(str(exp)) from exp
