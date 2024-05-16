# Third-party Libraries
from pydantic import BaseModel, Field

# Own Libraries
from apps.location.schema.response.interface import Response
from apps.location.schema.types.location import LocationType


class LocationMetadata(BaseModel):
    total_count: int = 0


class LocationListPayload(BaseModel):
    metadata: LocationMetadata
    items: list[LocationType] = Field(default_factory=list)

    @classmethod
    def empty_state(cls):
        return cls(metadata=LocationMetadata(), items=[])


class CreateLocationPayload(BaseModel):
    location: LocationType | None = None
    response: Response

    @classmethod
    def empty_state(cls, response: Response):
        return cls(location=None, response=response)
