# Standard Libraries
import logging

# Own Libraries
from apps.core.models import Category as CategoryModel
from apps.utils.decorator import async_database

logger = logging.getLogger(__name__)


class QueryCategoryProcess:
    """
    A class to handle querying operations for CategoryModel objects asynchronously.

    """

    @async_database()
    def get_objects(self, **kwargs) -> list[CategoryModel]:
        """
        Retrieve a list of CategoryModel objects based on the provided filters.
        """
        return list(CategoryModel.objects.filter(**kwargs))

    @async_database()
    def get_object(self, **kwargs) -> CategoryModel | None:
        """
        Retrieve a single CategoryModel object based on the provided filters.

        """
        return CategoryModel.objects.filter(**kwargs).first()


class EditionCategoryProcess:
    """
    A class to handle editing operations for CategoryModel objects asynchronously.

    """

    @async_database()
    def save_instance(
        self,
        instance_to_save: CategoryModel,
        update_fields: list[str] | None = None,
    ) -> CategoryModel:
        """
        Save the provided CategoryModel instance asynchronously.

        """
        instance_to_save.save(update_fields=update_fields)
        return instance_to_save

    @async_database()
    def get_or_create(self, **kwargs) -> CategoryModel:
        """
        Retrieve a CategoryModel object based on the provided filters or
        create it if it doesn't exist.

        """
        obj, _ = CategoryModel.objects.get_or_create(**kwargs)
        return obj


class CategoryProcess(
    QueryCategoryProcess,
    EditionCategoryProcess,
):
    """
    A combined class inheriting querying and editing operations for
    CategoryModel objects asynchronously.
    """

    pass
