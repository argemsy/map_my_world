# Third-party Libraries
from django.db import models
from django.utils.text import slugify

# Own Libraries
from apps.utils.models import AuditableMixin


class City(AuditableMixin):
    """
    A model to represent a city.

    Attributes:
        name (CharField): The name of the city.
        slug (SlugField): A slugified version of the city name, used for
            unique identification.
        country (ForeignKey): A foreign key relationship to the Country
            model, representing the country in which the city is located.
    """

    name = models.CharField(
        max_length=150,
        verbose_name="City name",
        db_index=True,
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )
    country = models.ForeignKey(
        "Country",
        on_delete=models.DO_NOTHING,
        related_name="cities_set",
    )

    class Meta:
        db_table = "city"
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self) -> str:
        return f"[{self.pk}] {self.name}"

    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        if not self.id:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
