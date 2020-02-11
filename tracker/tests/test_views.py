import pytest
from mixer.backend.django import mixer
from django.test import RequestFactory
from django.urls import reverse
from tracker.views import *
from tracker.models import Peak

pytestmark = pytest.mark.django_db


@pytest.fixture
def factory():
    return RequestFactory()


def test_home_view(factory):
    mixer.blend(Peak)
    path = reverse('home')
    request = factory.get(path)
    response = Home.as_view()(request)

    assert response.status_code == 200


def test_number_of_peaks_completed(factory):
    mixer.cycle(16).blend(Peak, complete=True)
    mixer.cycle(44).blend(Peak, complete=False)

    path = reverse('home')
    request = factory.get(path)
    view = Home()
    view.setup(request)
    view.object_list = view.get_queryset()
    context = view.get_context_data()

    assert context['number_of_peaks_completed'] == 16


def test_peak_detail_view(factory):
    mixer.blend(Peak, pk=6)
    path = reverse('peak_detail', kwargs={'pk': 6})
    request = factory.get(path)
    response = PeakDetail.as_view()(request, pk=6)

    assert response.status_code == 200


def test_peak_detail_get_interested_climbers_json(factory):
    peak = mixer.blend(Peak)
    climber = mixer.blend(User)
    climber2 = mixer.blend(User)
    interested_climber = mixer.blend(InterestedClimber, climber=climber, peak=peak)
    interested_climber2 = mixer.blend(InterestedClimber, climber=climber2, peak=peak)

    path = reverse('peak_detail', kwargs={'pk': peak.id})
    request = factory.get(path)

    view = PeakDetail()
    view.setup(request)

    response_json = '''
    [{
        "id": 2,
        "peak": 2,
        "first_name": "ray",
        "last_name": "dev"
    },
    {
        "id": 3,
        "peak": 5,
        "first_name": "ray",
        "last_name": "dev"
    },]
    '''


