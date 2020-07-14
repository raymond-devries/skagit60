import pytest
from tests.factories import *

pytestmark = pytest.mark.django_db


def test_peak_str():
    peak = PeakFactory(name="Baker, Mount")
    assert str(peak) == "Baker, Mount"


def test_tick_str():
    user = UserFactory(first_name="Alex", last_name="Honnold")
    peak = PeakFactory(name="Freerider")
    tick = TickFactory(climber=user, peak=peak)

    assert str(tick) == "Alex Honnold, Freerider"


def test_date_must_be_2020():
    with pytest.raises(ValidationError):
        TickFactory(date=datetime.date(2019, 12, 31))


def mark_peak_as_complete():
    peak = PeakFactory()
    TickFactory(peak=peak)

    assert peak.complete is True


def test_mark_peak_as_incomplete():
    peak = PeakFactory(complete=True)
    tick = TickFactory(peak=peak)
    tick.delete()

    assert peak.complete is False


def test_interest_peak_only_once():
    user = UserFactory()
    peak = PeakFactory()
    InterestedClimberFactory(climber=user, peak=peak)
    with pytest.raises(ValidationError):
        InterestedClimberFactory(climber=user, peak=peak)


def test_image_validation_too_many_images():
    trip_report = TripReportFactory()
    with pytest.raises(ValidationError):
        ReportImageFactory.create_batch(
            TripReport.max_images + 1, trip_report=trip_report
        )
