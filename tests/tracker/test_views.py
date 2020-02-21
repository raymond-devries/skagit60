import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from tracker.views import *
from tests.factories import *

pytestmark = pytest.mark.django_db


def test_home_view(rf):
    PeakFactory()
    path = reverse('home')
    request = rf.get(path)
    response = Home.as_view()(request)

    assert response.status_code == 200


def test_about_view(rf):
    path = reverse('about')
    request = rf.get(path)
    response = About.as_view()(request)

    assert response.status_code == 200


def test_number_of_peaks_completed(rf):
    PeakFactory.create_batch(16, complete=True)
    PeakFactory.create_batch(44, complete=False)

    path = reverse('home')
    request = rf.get(path)
    view = Home()
    view.setup(request)
    view.object_list = view.get_queryset()
    context = view.get_context_data()

    assert context['number_of_peaks_completed'] == 16


def test_peak_detail_view(rf):
    PeakFactory(pk=6)
    path = reverse('peak_detail', kwargs={'pk': 6})
    request = rf.get(path)
    response = PeakDetail.as_view()(request, pk=6)

    assert response.status_code == 200


def test_peak_detail_get_interested_climbers_json(rf):
    peak = PeakFactory()
    climber = UserFactory(first_name='Anna')
    climber2 = UserFactory(first_name='Bob')
    interested_climber = InterestedClimberFactory(climber=climber, peak=peak)
    interested_climber2 = InterestedClimberFactory(climber=climber2, peak=peak)

    path = reverse('peak_detail', kwargs={'pk': peak.id})
    request = rf.get(path)
    request.user = AnonymousUser

    view = PeakDetail()
    view.setup(request)
    view.kwargs = {'pk': 1}

    response_json = view.get_interested_climbers_json()
    response_json = json.loads(response_json)

    correct_json_as_py_object = \
        [{"id": interested_climber.id,
          "first_name": interested_climber.climber.first_name,
          "last_name": interested_climber.climber.last_name,
          "is_owner": False
          },
         {
             "id": interested_climber2.id,
             "first_name": interested_climber2.climber.first_name,
             "last_name": interested_climber2.climber.last_name,
             "is_owner": False
         }]

    assert response_json == correct_json_as_py_object


def test_peak_detail_get_ticks_json(rf):
    peak = PeakFactory(pk=1)
    tick1 = TickFactory(date=datetime.date(2020, 9, 6), peak=peak)
    tick2 = TickFactory(date=datetime.date(2020, 6, 17), peak=peak)

    path = reverse('peak_detail', kwargs={'pk': peak.id})
    request = rf.get(path)
    request.user = AnonymousUser()

    view = PeakDetail()
    view.setup(request)
    view.kwargs = {'pk': 1}

    response_json = view.get_ticks_json()
    response_json = json.loads(response_json)

    correct_json_as_py_object = \
        [{'id': tick1.id,
          'date': tick1.date.strftime(settings.REST_FRAMEWORK['DATE_FORMAT']),
          'first_name': tick1.climber.first_name,
          'last_name': tick1.climber.last_name,
          'is_owner': False
          },
         {
             'id': tick2.id,
             'date': tick2.date.strftime(settings.REST_FRAMEWORK['DATE_FORMAT']),
             'first_name': tick2.climber.first_name,
             'last_name': tick2.climber.last_name,
             'is_owner': False
         }]

    assert response_json == correct_json_as_py_object
