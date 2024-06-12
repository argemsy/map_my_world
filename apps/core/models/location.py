# Third-party Libraries
from django.db import models

# Own Libraries
from apps.utils.models import AuditableMixin


class Location(AuditableMixin):
    """
    A model to represent a geographical location.

    Attributes:
        country (ForeignKey): A foreign key relationship to the Country
            model, representing the country of the location.
        city (ForeignKey): A foreign key relationship to the City model,
            representing the city of the location.
        address (TextField): The address of the location.
        latitude (DecimalField): The latitude coordinate of the location.
        longitude (DecimalField): The longitude coordinate of the location.

    """

    country = models.ForeignKey(
        "Country",
        on_delete=models.DO_NOTHING,
        related_name="locations_set",
    )
    city = models.ForeignKey(
        "City",
        on_delete=models.DO_NOTHING,
        related_name="locations_set",
    )
    address = models.TextField(verbose_name="Location Address")
    latitude = models.DecimalField(
        verbose_name="Lat",
        max_digits=10,
        decimal_places=7,
        db_index=True,
    )
    longitude = models.DecimalField(
        verbose_name="Long",
        max_digits=10,
        decimal_places=7,
        db_index=True,
    )

    class Meta:
        db_table = "location"
        verbose_name = "Location"
        verbose_name_plural = "Location's"
        constraints = [
            models.UniqueConstraint(
                fields=["country", "city", "latitude", "longitude"],
                name="unique country, city, latitude and longitude",
                violation_error_message=(
                    "country, city, latitude and longitude cannot both be repeated"
                ),
            )
        ]

    def __str__(self) -> str:
        return f"[{self.id}] {self.address}"
