# Standard Libraries
from typing import Iterable

# Third-party Libraries
from pydantic import BaseModel, Field

# Own Libraries
from apps.location.schema.types.category import CategoryType
from apps.map_my_world.models import Category as CategoryModel
from apps.map_my_world.models import Location as LocationModel
from config.env_vars import settings


class LocationType(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float
    categories_set: list[CategoryType] = Field(default_factory=list)
    total_reviews: int | None = 0
    url_detail: str | None = None

    @classmethod
    def from_db_model(
        cls,
        instance: LocationModel,
        category_id: int,
        categories_list: Iterable[CategoryModel] | None = None,
    ) -> "LocationType":

        categories_list = categories_list or []
        categories = cls.get_category_types_list(categories_list=categories_list)
        return cls(
            id=instance.id,
            address=instance.address,
            latitude=instance.latitude,
            longitude=instance.longitude,
            categories_set=categories,
            url_detail=cls.get_url_detail(
                location_id=instance.id, category_id=category_id
            ),
            # annotate field's
            total_reviews=getattr(instance, "total_reviews", 0),
        )

    @staticmethod
    def get_url_detail(location_id: int, category_id: int) -> str:
        return f"{settings.SITE_URL}/api/rest/location-{location_id}/category-{category_id}"

    @staticmethod
    def get_category_types_list(
        categories_list: list[CategoryModel] | None = None,
    ) -> list[CategoryType]:
        if categories_list := categories_list or []:
            return [
                CategoryType.from_db_model(instance=category)
                for category in categories_list
            ]
        return []
