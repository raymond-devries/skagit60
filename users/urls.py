from django.urls import path, include
from users.views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile', Profile.as_view(), name='profile'),
    path('profile/edit/', EditProfile.as_view(), name='edit_profile')
]
