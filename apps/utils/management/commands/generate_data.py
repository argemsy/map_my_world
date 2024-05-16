# Third-party Libraries
from django.core.management.base import BaseCommand

# Own Libraries
from apps.map_my_world.models import Location, LocationCategory
from apps.utils.data_dummy.location import (
    LocationCategoryFactory,
    LocationFactory,
)


class Command(BaseCommand):
    help = "Export the first 50 records of MyModel"

    models = (
        (Location, "Location"),
        (LocationCategory, "LocationCategory"),
    )

    def handle(self, *args, **options):
        locations = LocationFactory.build_batch(size=1000)

        db_locations = Location.objects.bulk_create(objs=locations)
        for location in db_locations:

            LocationCategoryFactory.create(location_id=location.id)

        self.stdout.write(self.style.SUCCESS("Successfully exc"))
