from factory import Sequence, SubFactory, Faker
from factory.django import DjangoModelFactory

from hotel import models


class HotelFactory(DjangoModelFactory):
    name = Sequence(lambda n: "Hotel %d" % (n + 1))
    city = Faker("city")

    class Meta:
        model = models.Hotel


class GuestFactory(DjangoModelFactory):
    name = "Test"
    phone = Sequence(lambda n: "+316" + str(10_000_000 + n))
    language = models.Language.BRITISH_ENGLISH

    class Meta:
        model = models.Guest


class StayFactory(DjangoModelFactory):
    status = models.Stay.Status.UNKNOWN

    hotel = SubFactory(HotelFactory)
    guest = SubFactory(GuestFactory)

    class Meta:
        model = models.Stay
