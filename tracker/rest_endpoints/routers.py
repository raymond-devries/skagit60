from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .rest_views import *

router = DefaultRouter()

router.register('report_time', ReportTimeViewSet)

urlpatterns = [
    path
    ('', include(router.urls))
]
