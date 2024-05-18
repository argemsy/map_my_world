# Third-party Libraries
from pydantic import BaseModel

# Own Libraries
from apps.core.models import Category


class CategoryType(BaseModel):
    id: int
    name: str
    description: str | None = None

    @classmethod
    def from_db_model(cls, instance: Category) -> "CategoryType":
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
        )
