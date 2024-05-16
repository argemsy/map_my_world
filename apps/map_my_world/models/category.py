# Third-party Libraries
from django.db import models
from django.utils.text import slugify

# Own Libraries
from apps.utils.models import AuditableMixin


class Category(AuditableMixin):
    """
    A model to represent a category.

    Attributes:
        name (CharField): The name of the category.
        slug (SlugField): A slugified version of the category name, used
            for unique identification.
        description (TextField): A description of the category (optional).

    """

    name = models.CharField(verbose_name="Category name", max_length=150)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"[{self.id}]{self.name}"

    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        if not self.id:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
