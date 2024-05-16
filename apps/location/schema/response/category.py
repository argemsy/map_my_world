# Third-party Libraries
from pydantic import BaseModel

# Own Libraries
from apps.location.schema.response.interface import Response
from apps.location.schema.types.category import CategoryType


class CreateCategoryPayload(BaseModel):
    category: CategoryType | None = None
    response: Response

    @classmethod
    def empty_state(cls, response: Response):
        return cls(category=None, response=response)
