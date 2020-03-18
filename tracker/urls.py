from django.urls import path

from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about', About.as_view(), name='about'),
    path('peak/<int:pk>', PeakDetail.as_view(), name='peak_detail'),
    path('trip_report_view/<int:pk>', TripReportDetail.as_view(), name='trip_report_detail'),
    path('create_trip_report', TripReportCreate.as_view(), name='trip_report_create'),
    path('create_trip_report/<int:peak_id>', TripReportCreate.as_view(), name='trip_report_create_peak'),
    path('trip_report/<int:pk>', TripReportUpdate.as_view(), name='trip_report_update'),
    path('delete_trip_report/<int:pk>', TripReportDelete.as_view(), name='trip_report_delete'),
    path('trip_reports', TripReports.as_view(), name='trip_reports'),
    path('leader_board', LeaderBoard.as_view(), name='leader_board'),
    path('map', Map.as_view(), name='map'),
    path('status', Status.as_view(), name='status'),
    path('loaderio-ae015b95ea02363e914209fe5f684554', LoaderVerification.as_view(), name='loader_verification')
]
