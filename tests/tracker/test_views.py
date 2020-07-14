import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from tracker.views import *
from tests.factories import *

pytestmark = pytest.mark.django_db


class TestHomeView:
    @pytest.fixture
    def setup_home_view(self, rf):
        PeakFactory.create_batch(16, complete=True)
        PeakFactory.create_batch(44, complete=False)

        path = reverse("home")
        request = rf.get(path)
        view = Home()
        view.setup(request)
        view.object_list = view.get_queryset()

        return view

    def test_home_view(self, rf):
        PeakFactory()
        path = reverse("home")
        request = rf.get(path)
        response = Home.as_view()(request)

        assert response.status_code == 200

    def test_home_view_number_of_peaks_completed(self, setup_home_view):
        context = setup_home_view.get_context_data()

        assert context["number_of_peaks_completed"] == 16


def test_about_view(rf):
    path = reverse("about")
    request = rf.get(path)
    response = About.as_view()(request)

    assert response.status_code == 200


class TestPeakDetailView:
    @pytest.fixture
    def setup_peak_detail_view(self, rf):
        peak = PeakFactory(pk=1)
        climber = UserFactory(first_name="Anna", last_name="Smith")
        climber2 = UserFactory(first_name="Bob", last_name="Johnson")
        InterestedClimberFactory(pk=567, climber=climber, peak=peak)
        InterestedClimberFactory(pk=219, climber=climber2, peak=peak)
        TickFactory(pk=6788, date=datetime.date(2020, 9, 6), peak=peak, climber=climber)
        TickFactory(
            pk=920, date=datetime.date(2020, 6, 17), peak=peak, climber=climber2
        )
        TripReportFactory(pk=543, peak=peak)

        path = reverse("peak_detail", kwargs={"pk": 1})
        request = rf.get(path)
        request.user = AnonymousUser

        view = PeakDetail()
        view.setup(request)
        view.kwargs = {"pk": 1}
        view.object = view.get_object()

        return view

    def test_peak_detail_view_status_code(self, setup_peak_detail_view):
        assert setup_peak_detail_view.response_class.status_code == 200

    def test_peak_detail_ticks_context(self, setup_peak_detail_view):
        expected_tick_context = setup_peak_detail_view.get_ticks_json()
        context = setup_peak_detail_view.get_context_data()
        assert context["ticks"] == expected_tick_context

    def test_peak_detail_interested_climbers_context(self, setup_peak_detail_view):
        expected_interested_climber_context = (
            setup_peak_detail_view.get_interested_climbers_json()
        )
        context = setup_peak_detail_view.get_context_data()
        assert context["interested_climbers"] == expected_interested_climber_context

    def test_peak_detail_reports_context(self, setup_peak_detail_view):
        expected_reports_context = TripReport.objects.filter(pk=543)
        context = setup_peak_detail_view.get_context_data()
        assert list(context["reports"]) == list(expected_reports_context)

    def test_peak_detail_get_interested_climbers_json(self, setup_peak_detail_view):
        response_json = setup_peak_detail_view.get_interested_climbers_json()
        response_json = json.loads(response_json)

        expected_json_as_py_object = [
            {"id": 567, "first_name": "Anna", "last_name": "Smith", "is_owner": False},
            {"id": 219, "first_name": "Bob", "last_name": "Johnson", "is_owner": False},
        ]

        assert response_json == expected_json_as_py_object

    def test_peak_detail_get_ticks_json(self, setup_peak_detail_view):
        response_json = setup_peak_detail_view.get_ticks_json()
        response_json = json.loads(response_json)

        expected_json_as_py_object = [
            {
                "id": 6788,
                "date": datetime.date(2020, 9, 6).strftime(
                    settings.REST_FRAMEWORK["DATE_FORMAT"]
                ),
                "first_name": "Anna",
                "last_name": "Smith",
                "is_owner": False,
            },
            {
                "id": 920,
                "date": datetime.date(2020, 6, 17).strftime(
                    settings.REST_FRAMEWORK["DATE_FORMAT"]
                ),
                "first_name": "Bob",
                "last_name": "Johnson",
                "is_owner": False,
            },
        ]

        assert response_json == expected_json_as_py_object


class TestTripReportDetailView:
    @pytest.fixture
    def setup_trip_report_detail_view(self, rf):
        trip_report = TripReportFactory(
            pk=1, start=datetime.date(2020, 2, 6), end=datetime.date(2020, 2, 7)
        )
        user1 = UserFactory(first_name="Chris", last_name="Sharma")
        user2 = UserFactory(first_name="Adam", last_name="Ondra")
        ReportImageFactory(pk=1, trip_report=trip_report)
        ReportImageFactory(pk=2, trip_report=trip_report)
        ReportTimeFactory(pk=1, trip_report=trip_report)
        ReportTimeFactory(pk=2, trip_report=trip_report)
        comment1 = ReportCommentFactory(
            pk=739, trip_report=trip_report, comment="Wow that is great", user=user1
        )
        comment1.time = datetime.datetime(2020, 3, 5, 8, 0, 0)
        comment1.save()
        comment2 = ReportCommentFactory(
            pk=274, trip_report=trip_report, comment="Way to send it!", user=user2
        )
        comment2.time = datetime.datetime(2020, 3, 5, 7, 0, 0)
        comment2.save()

        path = reverse("trip_report_detail", kwargs={"pk": 1})
        request = rf.get(path)
        request.user = AnonymousUser

        view = TripReportDetail()
        view.setup(request)
        view.kwargs = {"pk": 1}
        view.object = view.get_object()

        return view

    def test_peak_detail_view_status_code(self, setup_trip_report_detail_view):
        assert setup_trip_report_detail_view.response_class.status_code == 200

    def test_peak_detail_show_end_context_end_date_different(
        self, setup_trip_report_detail_view
    ):
        context = setup_trip_report_detail_view.get_context_data()
        assert context["show_end"] is True

    def test_peak_detail_show_end_context_end_date_none(
        self, setup_trip_report_detail_view
    ):
        trip_report = TripReport.objects.get(pk=1)
        trip_report.end = None
        trip_report.save()
        context = setup_trip_report_detail_view.get_context_data()
        assert context["show_end"] is False

    def test_peak_detail_show_end_context_end_date_same_as_start(
        self, setup_trip_report_detail_view
    ):
        trip_report = TripReport.objects.get(pk=1)
        trip_report.end = datetime.date(2020, 2, 6)
        trip_report.save()
        context = setup_trip_report_detail_view.get_context_data()
        assert context["show_end"] is False

    def test_peak_detail_context_images(self, setup_trip_report_detail_view):
        context = setup_trip_report_detail_view.get_context_data()
        expected_images = ReportImage.objects.filter(pk__range=(1, 2))
        assert list(context["images"]) == list(expected_images)

    def test_peak_detail_context_times(self, setup_trip_report_detail_view):
        context = setup_trip_report_detail_view.get_context_data()
        expected_times = ReportTime.objects.filter(pk__range=(1, 2))
        assert list(context["times"]) == list(expected_times)

    def test_peak_detail_get_comments_json(self, setup_trip_report_detail_view):
        report = setup_trip_report_detail_view.get_object()
        response_json = setup_trip_report_detail_view.get_comments_json(report)
        response_json = json.loads(response_json)

        expected_json_as_py_object = [
            {
                "id": 739,
                "comment": "Wow that is great",
                "time": datetime.datetime(2020, 3, 5, 16, 0, 0).strftime(
                    settings.REST_FRAMEWORK["DATETIME_FORMAT"]
                ),
                "first_name": "Chris",
                "last_name": "Sharma",
                "is_owner": False,
            },
            {
                "id": 274,
                "comment": "Way to send it!",
                "time": datetime.datetime(2020, 3, 5, 15, 0, 0).strftime(
                    settings.REST_FRAMEWORK["DATETIME_FORMAT"]
                ),
                "first_name": "Adam",
                "last_name": "Ondra",
                "is_owner": False,
            },
        ]

        assert response_json == expected_json_as_py_object


class TestReportCreate:
    def test_trip_report_create_no_kwarg(self, client):
        user = UserFactory()

        path = reverse("trip_report_create")
        client.force_login(user)
        client.get(path)

        assert TripReport.objects.filter(writer=user).exists()

    def test_trip_report_create_kwarg(self, client):
        user = UserFactory()
        peak = PeakFactory(pk=1)

        client.force_login(user)
        client.get("/create_trip_report/1")

        assert TripReport.objects.filter(writer=user, peak=peak).exists()

    def test_trip_report_create_incorrect_kwarg(self, client):
        user = UserFactory()

        client.force_login(user)
        response = client.get("/create_trip_report/56")

        assert response.status_code == 404


class TestTripReportUpdate:
    @pytest.fixture
    def setup_trip_report_update_view(self, rf):
        user = UserFactory()
        trip_report = TripReportFactory(pk=1, writer=user, published=False)
        ReportTimeFactory(trip_report=trip_report, pk=1, time=6)
        ReportTimeFactory(trip_report=trip_report, pk=2, time=7)
        ReportImageFactory(trip_report=trip_report, pk=1)
        ReportImageFactory(trip_report=trip_report, pk=2)

        path = reverse("trip_report_update", kwargs={"pk": 1})
        request = rf.get(path)
        request.user = user

        view = TripReportUpdate()
        view.setup(request)
        view.kwargs = {"pk": 1}
        view.object = view.get_object()

        return view

    def test_trip_report_update_status_code(self, setup_trip_report_update_view):
        assert setup_trip_report_update_view.response_class.status_code == 200

    def test_trip_report_update_form_valid_not_published(
        self, setup_trip_report_update_view
    ):
        form = setup_trip_report_update_view.get_form()
        setup_trip_report_update_view.form_valid(form)

        assert setup_trip_report_update_view.get_object().published is False

    def test_trip_report_update_form_valid_published(
        self, setup_trip_report_update_view
    ):
        form = setup_trip_report_update_view.get_form()
        post_request = setup_trip_report_update_view.request.POST
        post_request._mutable = True
        post_request["publish_report"] = "Publish Report"
        setup_trip_report_update_view.form_valid(form)

        assert setup_trip_report_update_view.get_object().published is True

    def test_trip_report_update_get_context_max_images(
        self, setup_trip_report_update_view
    ):
        context = setup_trip_report_update_view.get_context_data()
        assert context["max_uploads"] == TripReport.max_images - 2

    def test_trip_report_update_get_images(self, setup_trip_report_update_view):
        report = setup_trip_report_update_view.get_object()
        expected_images = ReportImage.objects.filter(pk__range=(1, 2))
        (
            response_images,
            response_images_json,
        ) = setup_trip_report_update_view.get_images(report)
        expected_json_as_py_object = {
            "1": {"id": 1, "url": expected_images[0].image.url},
            "2": {"id": 2, "url": expected_images[1].image.url},
        }

        assert list(response_images) == list(expected_images)
        assert json.loads(response_images_json) == expected_json_as_py_object

    def test_trip_report_update_get_report_times_json(
        self, setup_trip_report_update_view
    ):
        report = setup_trip_report_update_view.get_object()
        time1 = ReportTime.objects.get(pk=1)
        time2 = ReportTime.objects.get(pk=2)
        expected_json_as_py_object = {
            "1": {
                "start_point_display": time1.get_start_point_display(),
                "end_point_display": time1.get_end_point_display(),
                "time": "6.0",
                "id": 1,
            },
            "2": {
                "start_point_display": time2.get_start_point_display(),
                "end_point_display": time2.get_end_point_display(),
                "time": "7.0",
                "id": 2,
            },
        }

        response_json = setup_trip_report_update_view.get_report_times_json(report)
        assert json.loads(response_json) == expected_json_as_py_object


class TestTripReportDelete:
    def test_delete_trip_report_success(self, client):
        user = UserFactory()
        TripReportFactory(pk=1, writer=user)

        client.force_login(user)
        path = reverse("trip_report_delete", kwargs={"pk": 1})
        client.post(path)

        assert not TripReport.objects.filter(pk=1).exists()

    def test_delete_trip_report_failure(self, client):
        user = UserFactory()
        TripReportFactory(pk=1)

        client.force_login(user)
        path = reverse("trip_report_delete", kwargs={"pk": 1})
        client.post(path)

        assert TripReport.objects.filter(pk=1).exists()


def test_leader_board_view(rf):
    path = reverse("leader_board")
    request = rf.get(path)
    response = About.as_view()(request)

    assert response.status_code == 200


class TestTripReportsView:
    @pytest.fixture
    def setup_trip_reports_view(self, rf):
        TripReportFactory.create_batch(6, published=True)
        TripReportFactory.create_batch(9, published=False)
        path = reverse("trip_reports")
        request = rf.get(path)
        request.user = AnonymousUser

        view = TripReports()
        view.setup(request)

        return view

    def test_trip_reports_status_code(self, setup_trip_reports_view):
        assert setup_trip_reports_view.response_class.status_code == 200

    def test_trip_reports_queryset(self, setup_trip_reports_view):
        assert setup_trip_reports_view.queryset.count() == 6


def test_loader_verification_view(rf):
    path = reverse("loader_verification")
    request = rf.get(path)
    response = About.as_view()(request)

    assert response.status_code == 200


def test_status_view(rf):
    path = reverse("status")
    request = rf.get(path)
    response = About.as_view()(request)

    assert response.status_code == 200
