from django.urls import reverse, resolve


def test_peak_detail_url():
    path = reverse("peak_detail", kwargs={"pk": 1})
    assert resolve(path).view_name == "peak_detail"


def test_about_url():
    path = reverse("about")
    assert resolve(path).view_name == "about"


def test_trip_report_detail_url():
    path = reverse("trip_report_detail", kwargs={"pk": 1})
    assert resolve(path).view_name == "trip_report_detail"


def test_create_trip_report_url():
    path = reverse("trip_report_create")
    assert resolve(path).view_name == "trip_report_create"


def test_create_trip_report_peak_url():
    path = reverse("trip_report_create_peak", args=[1])
    assert resolve(path).view_name == "trip_report_create_peak"


def test_trip_report_update_url():
    path = reverse("trip_report_update", kwargs={"pk": 1})
    assert resolve(path).view_name == "trip_report_update"


def test_trip_report_delete_url():
    path = reverse("trip_report_delete", kwargs={"pk": 1})
    assert resolve(path).view_name == "trip_report_delete"


def test_leader_board_url():
    path = reverse("leader_board")
    assert resolve(path).view_name == "leader_board"


def test_loader_verification_url():
    path = reverse("loader_verification")
    assert resolve(path).view_name == "loader_verification"
