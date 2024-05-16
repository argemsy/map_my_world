# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.map_my_world.models import (
    Category,
    City,
    Country,
    Location,
    LocationCategory,
)

# Register your models here.
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(LocationCategory)
