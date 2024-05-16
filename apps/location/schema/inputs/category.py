# Third-party Libraries
from pydantic import BaseModel, field_validator


class CategoryAddInput(BaseModel):
    name: str
    description: str | None = None

    @field_validator("name", mode="before")
    @classmethod
    def _check_name(cls, name: str):
        name = name.strip()
        if len(name) > 150:
            raise AssertionError(
                "The input for 'name' is invalid; maximum characters allowed is 150"
            )
        return name

    @field_validator("description", mode="before")
    @classmethod
    def _check_description(cls, description: str | None = None):
        if description:
            description = description.strip()
            if len(description) > 500:
                raise AssertionError(
                    "The input for 'description' is invalid; maximum "
                    "characters allowed is 500"
                )
        return description
