from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('peak/<int:pk>/', PeakDetail.as_view(), name='peak_detail'),
    path('trip_report_view/<int:pk>/', TripReportDetail.as_view(), name='trip_report_detail'),
    path('create_trip_report', TripReportCreate.as_view(), name='trip_report_create'),
    path('trip_report/<int:pk>/', TripReportUpdate.as_view(), name='trip_report_update'),
    path('delete_trip_report/<int:pk>/', TripReportDelete.as_view(), name='trip_report_delete'),
    path('tick', TickCreate.as_view(), name='tick_create'),
    path('tick_delete/<int:pk>/', TickDelete.as_view(), name='tick_delete')
]
