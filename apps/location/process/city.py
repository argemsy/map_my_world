# Standard Libraries
import logging

# Own Libraries
from apps.map_my_world.models import City as CityModel
from apps.map_my_world.models import Country as CountryModel
from apps.utils.decorator import async_database

logger = logging.getLogger(__name__)


class QueryCityProcess:
    """
    A class to handle querying operations for City objects asynchronously.

    """

    @async_database()
    def get_city_and_country(self) -> dict[int, tuple[CityModel, CountryModel]]:
        queryset = CityModel.objects.filter(is_deleted=False)
        return {city.id: (city, city.country) for city in queryset}


class EditionCityProcess:
    """
    A class to handle editing operations for City objects asynchronously.

    """

    pass


class CityProcess(
    QueryCityProcess,
    EditionCityProcess,
):
    """
    A combined class inheriting querying and editing operations for
    City objects asynchronously.
    """

    pass
