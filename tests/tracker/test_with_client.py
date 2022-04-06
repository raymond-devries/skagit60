import pytest

from tests.factories import *

pytestmark = pytest.mark.django_db


@pytest.fixture
def mock_db_return_user():
    user = UserFactory()
    peak = PeakFactory(pk=1)
    TickFactory(peak=peak, climber=user)
    InterestedClimberFactory(peak=peak, climber=user)
    trip_report = TripReportFactory(pk=1, peak=peak, writer=user)
    ReportTimeFactory.create_batch(3, trip_report=trip_report)
    ReportImageFactory.create_batch(6, trip_report=trip_report)
    ReportCommentFactory.create_batch(3, trip_report=trip_report)

    return user


anonymous_user_urls = [
    ("/", 200),
    ("/about", 200),
    ("/peak/1", 200),
    ("/trip_report_view/1", 200),
    ("/create_trip_report", 302),
    ("/create_trip_report/1", 302),
    ("/create_trip_report/684756", 302),
    ("/trip_report/56758765", 302),
    ("/delete_trip_report/1", 302),
    ("/trip_reports", 200),
    ("/leader_board", 200),
]


@pytest.mark.parametrize("url, status_code", anonymous_user_urls)
def test_anonymous_client_status_codes(url, status_code, client, mock_db_return_user):
    response = client.get(url)
    assert response.status_code == status_code


logged_in_user_urls = [
    ("/", 200),
    ("/about", 200),
    ("/peak/1", 200),
    ("/trip_report_view/1", 200),
    ("/create_trip_report", 302),
    ("/create_trip_report/1", 302),
    ("/create_trip_report/684756", 404),
    ("/trip_report/1", 200),
    ("/trip_report/87309753", 404),
    ("/delete_trip_report/1", 200),
    ("/delete_trip_report/5436123", 404),
    ("/trip_reports", 200),
    ("/leader_board", 200),
]


@pytest.mark.parametrize("url, status_code", logged_in_user_urls)
def test_logged_in_client_status_codes(url, status_code, client, mock_db_return_user):
    client.force_login(mock_db_return_user)
    response = client.get(url)
    assert response.status_code == status_code
