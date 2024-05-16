# Standard Libraries
import logging

# Third-party Libraries
from django.db import connection, models

logger = logging.getLogger(__name__)


class AuditableMixin(models.Model):
    created_at: str = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Fecha de Creación",
    )
    updated_at: str = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de modificación",
    )
    is_deleted: bool = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        abstract = True

    @classmethod
    def truncate(cls):
        """
        Truncate Table and Restart index.
        How to use:
        - cls.truncate()
        """
        try:
            db_table = cls._meta.db_table

            sql = f"TRUNCATE TABLE {db_table} RESTART IDENTITY CASCADE;"
            with connection.cursor() as cursor:
                cursor.execute(sql)
            logger.info(f"*** {db_table}.truncate table success!!! ***")
        except Exception as exp:
            error = str(exp)
            logger.error(
                f"***Error: {db_table}.truncate : {error} - {repr(exp)}***",
                exc_info=True,
            )
