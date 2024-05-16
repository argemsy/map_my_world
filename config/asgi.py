"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# Standard Libraries
import os

# Third-party Libraries
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

application = get_asgi_application()
# Third-party Libraries
from fastapi import FastAPI

# Own Libraries
from apps.map_my_world.category_router import add_category_tag, category_router
from apps.map_my_world.location_router import (
    add_location_tag,
    location_detail_tag,
    location_router,
    recommend_locations_tag,
)

metadata_tags = [
    add_category_tag,
    add_location_tag,
    recommend_locations_tag,
    location_detail_tag,
]

fastapp = FastAPI(
    openapi_tags=[tag.dict(by_alias=True) for tag in metadata_tags],
)


fastapp.include_router(
    location_router,
    prefix="/api/rest",
)
fastapp.include_router(
    category_router,
    prefix="/api/rest",
)
