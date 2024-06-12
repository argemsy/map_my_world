# Third-party Libraries
from django.db import models

# Own Libraries
from apps.utils.models import AuditableMixin


class LocationCategory(AuditableMixin):
    """
    A model to represent the relationship between a location and a category.

    Attributes:
        location (ForeignKey): A foreign key relationship to the Location
            model, representing the location associated with the category.
        category (ForeignKey): A foreign key relationship to the Category
            model, representing the category associated with the location.

    """

    location = models.ForeignKey(
        "Location",
        on_delete=models.PROTECT,
        related_name="locations_categories_set",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="locations_categories_set",
    )
    total_reviews = models.IntegerField(
        verbose_name="Total reviews",
        default=0,
        db_index=True,
    )

    class Meta:
        db_table = "location_category"
        verbose_name = "Location category"
        verbose_name_plural = "Location categories"
        constraints = [
            models.UniqueConstraint(
                fields=["location", "category"],
                name="unique category for location",
                violation_error_message="location and category cannot both be repeated",
            )
        ]

    def __str__(self) -> str:
        return f"[{self.id}] {self.location.address} ({self.category.name})"
