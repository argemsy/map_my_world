# Standard Libraries
import logging

# Own Libraries
from apps.map_my_world.models import Category as CategoryModel
from apps.utils.decorator import async_database

logger = logging.getLogger(__name__)


class QueryCategoryProcess:
    @async_database()
    def get_objects(self, **kwargs) -> list[CategoryModel]:
        return list(CategoryModel.objects.filter(**kwargs))

    @async_database()
    def get_object(self, **kwargs) -> CategoryModel | None:
        return CategoryModel.objects.filter(**kwargs).first()


class EditionCategoryProcess:

    @async_database()
    def save_instance(
        self,
        instance_to_save: CategoryModel,
        update_fields: list[str] | None = None,
    ) -> CategoryModel:
        instance_to_save.save(update_fields=update_fields)
        return instance_to_save

    @async_database()
    def get_or_create(self, **kwargs) -> CategoryModel:
        obj, _ = CategoryModel.objects.get_or_create(**kwargs)
        return obj


class CategoryProcess(
    QueryCategoryProcess,
    EditionCategoryProcess,
):
    pass
