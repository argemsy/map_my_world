# Standard Libraries
import functools
import logging
from functools import wraps
from typing import Union

# Third-party Libraries
from asgiref.sync import sync_to_async
from django.db import close_old_connections, utils
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# Own Libraries
from apps.location.schema.response.category import CreateCategoryPayload
from apps.location.schema.response.interface import Response
from apps.location.schema.response.location import CreateLocationPayload

logger = logging.getLogger(__name__)

PayloadClass = Union[CreateCategoryPayload, CreateLocationPayload]


def async_database():
    def decorator(func):
        @sync_to_async(thread_sensitive=True)
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (utils.InterfaceError, utils.OperationalError):
                close_old_connections()
                logger.info("database:close_old_connections()")
                return func(*args, **kwargs)

        return wrapper

    return decorator


def handler_exception(payload_class: PayloadClass, log_tag: str):
    """
    Decorator for handling exceptions in asynchronous functions.

    Args:
        payload_class (PayloadClass): The class for generating empty states of payload.
        log_tag (str): Tag to identify the log entry.

    Returns:
        Callable: Decorator function.

    Example:
        @handler_exception(MyPayloadClass, "my_tag")
        async def my_async_function():
            ...
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except (AssertionError, ValidationError) as exp:
                logger.warning(
                    f"***{log_tag}, Validation Error, {repr(exp)}", exc_info=True
                )

                content = payload_class.empty_state(
                    response=Response(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        type="Validation Error",
                        message=str(exp),
                    )
                )
                return JSONResponse(
                    content=content.model_dump(),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as exp:
                logger.error(
                    f"***{log_tag}, Internal Error, {repr(exp)}", exc_info=True
                )
                content = payload_class.empty_state(
                    response=Response(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        type="Internal Error",
                        message=None,
                    )
                )
                return JSONResponse(
                    content=content.model_dump(),
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return wrapper

    return decorator
