# Standard Libraries
from typing import Iterable

# Third-party Libraries
from pydantic import BaseModel, Field

# Own Libraries
from apps.location.schema.types.category import CategoryType
from apps.location.schema.types.city import CityType
from apps.core.models import Category as CategoryModel
from apps.core.models import City as CityModel
from apps.core.models import Country as CountryModel
from apps.core.models import Location as LocationModel
from config.env_vars import settings


class LocationType(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float
    categories_set: list[CategoryType] = Field(default_factory=list)
    city: CityType | None = None
    total_reviews: int | None = 0
    url_detail: str | None = None

    @classmethod
    def from_db_model(
        cls,
        instance: LocationModel,
        category_id: int,
        city_tuple: tuple[CityModel, CountryModel],
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
            city=cls.get_city_type(city_tuple=city_tuple),
            url_detail=cls.get_url_detail(
                location_id=instance.id, category_id=category_id
            ),
            # annotate field's
            total_reviews=getattr(instance, "total_reviews", 0),
        )

    @staticmethod
    def get_city_type(city_tuple: tuple[CityModel, CountryModel]) -> CityType | None:
        if city_tuple:
            city, country = city_tuple
            return CityType.from_db_model(instance=city, country=country)

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
