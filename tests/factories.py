import factory.random
from factory import Faker, SubFactory, django
from factory.django import DjangoModelFactory

from tracker.models import *

factory.random.reseed_random("skagit60")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    username = Faker("pystr", min_chars=12)


class PeakFactory(DjangoModelFactory):
    class Meta:
        model = Peak

    name = Faker("sentence", nb_words=2)
    display_name = Faker("sentence", nb_words=2)
    elevation = Faker("random_int", min=0, max=10000)
    lat = Faker("latitude")
    long = Faker("longitude")
    peakbagger_link = Faker("url")
    complete = Faker("boolean")


class TickFactory(DjangoModelFactory):
    class Meta:
        model = Tick

    climber = SubFactory(UserFactory)
    peak = SubFactory(PeakFactory)
    date = Faker(
        "date_between_dates",
        date_start=datetime.date(2020, 1, 1),
        date_end=datetime.date(2021, 1, 1),
    )


class InterestedClimberFactory(DjangoModelFactory):
    class Meta:
        model = InterestedClimber

    climber = SubFactory(UserFactory)
    peak = SubFactory(PeakFactory)


class TripReportFactory(DjangoModelFactory):
    class Meta:
        model = TripReport

    writer = SubFactory(UserFactory)
    peak = SubFactory(PeakFactory)
    published = True
    permits = Faker("sentence", nb_words=2)
    start = Faker(
        "date_between_dates",
        date_start=datetime.date(2020, 1, 1),
        date_end=datetime.date(2021, 1, 1),
    )
    end = Faker(
        "date_between_dates",
        date_start=datetime.date(2020, 1, 1),
        date_end=datetime.date(2021, 1, 1),
    )
    difficulty = Faker("random_int", min=1, max=4)
    route_name = Faker("sentence", nb_words=2)
    snow_level = Faker("random_int", min=0, max=14999)
    weather = Faker("text")
    gear = Faker("text")
    report = Faker("text", max_nb_chars=5000)


class ReportTimeFactory(DjangoModelFactory):
    class Meta:
        model = ReportTime

    trip_report = SubFactory(TripReportFactory)
    start_point = Faker("random_choices", elements=("TH", "C", "S"))
    end_point = Faker("random_choices", elements=("TH", "C", "S"))
    time = Faker("pydecimal", left_digits=2, right_digits=1, positive=True)


class ReportImageFactory(DjangoModelFactory):
    class Meta:
        model = ReportImage

    trip_report = SubFactory(TripReportFactory)
    image = django.ImageField()


class ReportCommentFactory(DjangoModelFactory):
    class Meta:
        model = ReportComment

    user = SubFactory(UserFactory)
    trip_report = SubFactory(TripReportFactory)

    comment = Faker("text", max_nb_chars=1000)
