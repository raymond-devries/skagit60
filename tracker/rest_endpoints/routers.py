from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .rest_views import *

router = DefaultRouter()

router.register('report_time', ReportTimeViewSet)
router.register('report_image', ReportImageViewSet)
router.register('tick', TickViewSet)
router.register('interested_climber', InterestedClimberViewSet)
router.register('report_comment', ReportCommentViewSet)

urlpatterns = [
    path
    ('', include(router.urls))
]
