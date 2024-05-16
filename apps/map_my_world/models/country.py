# Third-party Libraries
from django.db import models
from django.utils.text import slugify

# Own Libraries
from apps.utils.models import AuditableMixin


class Country(AuditableMixin):
    """
    A model to represent a country.

    Attributes:
        name (CharField): The name of the country.
        slug (SlugField): A slugified version of the country name, used
            for unique identification.
        code (CharField): The country code, a short identifier for the
            country.
    """

    name = models.CharField(
        max_length=150,
        verbose_name="Country name",
        db_index=True,
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )
    code = models.CharField(
        max_length=10,
        verbose_name="Country Code",
        help_text="Ex: Colombia => (co)",
    )

    def __str__(self) -> str:
        return f"[{self.pk}] {self.name}"

    class Meta:
        db_table = "country"
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        if not self.id:
            self.slug = slugify(self.name)
        if _code := self.code:
            self.code = _code.upper()
        return super().save(*args, **kwargs)
