from pydantic import BaseModel

from apps.core.models import City as CityModel
from apps.core.models import Country as CountryModel


class CountryType(BaseModel):
    id: int
    name: str
    code: str

    @classmethod
    def from_db_model(cls, instance: CountryModel) -> "CountryType":
        return cls(
            id=instance.id,
            name=instance.name,
            code=instance.code,
        )


class CityType(BaseModel):
    id: int
    name: str
    country: CountryType

    @classmethod
    def from_db_model(cls, instance: CityModel, country: CountryModel) -> "CityType":
        return cls(
            id=instance.id,
            name=instance.name,
            country=cls.get_country(instance=country),
        )

    @staticmethod
    def get_country(instance: CountryModel):
        return CountryType.from_db_model(instance=instance)
