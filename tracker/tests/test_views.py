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
    mixer.cycle(44).blend(Peak)

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

