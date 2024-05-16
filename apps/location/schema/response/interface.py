# Third-party Libraries
from pydantic import BaseModel


class Response(BaseModel):
    status_code: int
    type: str
    message: str | None = None
