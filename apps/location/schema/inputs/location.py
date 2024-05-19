# Third-party Libraries
from pydantic import BaseModel, PositiveInt, field_validator

# Own Libraries
from apps.location.schema.enums.location import LocationFieldEnum
from apps.utils.enums import SortedOrderByFieldEnum


class CreateLocationInput(BaseModel):
    country_id: PositiveInt
    city_id: PositiveInt
    address: str
    latitude: float
    longitude: float

    @field_validator("address", mode="before")
    @classmethod
    def _check_address(cls, address: str):
        address = address.strip()
        if len(address) > 500:
            raise AssertionError(
                "The input for 'address' is invalid; maximum "
                "characters allowed is 500"
            )
        return address


class LocationAddInput(BaseModel):
    category_id_list: list[PositiveInt]
    location: CreateLocationInput
