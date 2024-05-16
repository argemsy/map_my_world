# Standard Libraries
import logging

# Third-party Libraries
from fastapi import APIRouter, status

# Own Libraries
from apps.location.process.category import CategoryProcess
from apps.location.schema.inputs.category import CategoryAddInput
from apps.location.schema.response.category import CreateCategoryPayload, Response
from apps.location.schema.types.category import CategoryType
from apps.utils.decorator import handler_exception
from apps.utils.tags import MetadataTag

category_router = APIRouter()

logger = logging.getLogger(__name__)

add_category_tag = MetadataTag(
    name="Add Categories",
    description=(
        """Add a new category based on the input data =>
        [
            CategoryAddInput(
                name='New Category',
                description='Description of the category'
            )
        ]
        """
    ),
)


@category_router.post(
    "/add-categories",
    status_code=status.HTTP_201_CREATED,
    tags=[add_category_tag.name],
)
@handler_exception(payload_class=CreateCategoryPayload, log_tag="Add Categories")
async def add_categories(input: CategoryAddInput) -> CreateCategoryPayload:
    process = CategoryProcess()
    kwargs = input.model_dump()

    new_category = await process.get_or_create(**kwargs)

    return CreateCategoryPayload(
        category=CategoryType.from_db_model(instance=new_category),
        response=Response(
            status_code=status.HTTP_201_CREATED,
            type="Success",
            message="",
        ),
    )
