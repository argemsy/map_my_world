# Third-party Libraries
import factory
from factory.django import DjangoModelFactory

# Own Libraries
from apps.core.models import Location, LocationCategory


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location

    country_id = factory.Faker("random_int", min=1, max=3)
    city_id = factory.SelfAttribute("country_id")
    address = factory.Faker("address")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")


class LocationCategoryFactory(DjangoModelFactory):
    class Meta:
        model = LocationCategory

    location = factory.SubFactory(LocationFactory)
    category_id = factory.Faker("random_int", min=1, max=5)
    total_reviews = factory.Faker("random_int", min=0, max=100)
