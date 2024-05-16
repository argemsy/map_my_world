# Third-party Libraries
from django.core import serializers
from django.core.management.base import BaseCommand

# Own Libraries
from apps.map_my_world.models import Location, LocationCategory


class Command(BaseCommand):
    help = "Export the first 50 records of MyModel"

    models = (
        (Location, "Location"),
        (LocationCategory, "LocationCategory"),
    )

    def handle(self, *args, **options):
        # Obtener los primeros 10 registros del modelo
        for model, model_name in self.models:
            first_50_records = model.objects.all().order_by("id")

            # Serializar los registros en formato JSON
            data = serializers.serialize("json", first_50_records)

            # Guardar los datos en un archivo
            with open(f"apps/utils/fixtures/json/{model_name}.json", "w") as file:
                file.write(data)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully exported the first 50 records to model_data.json"
            )
        )
