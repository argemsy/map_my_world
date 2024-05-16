from pydantic import BaseModel


class MetadataTag(BaseModel):
    name: str
    description: str | None = None

    class Config:
        allow_population_by_field_name = True
