from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('peak/<int:pk>/', PeakDetail.as_view(), name='peak_detail')

]