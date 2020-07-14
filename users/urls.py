from django.urls import path, include
from .views import *

urlpatterns = [
    path("login/", CustomLogin.as_view(), name="login"),
    path("signup/", Signup.as_view(), name="signup"),
    path(
        "account_activation_sent/",
        AccountActivationSent.as_view(),
        name="account_activation_sent",
    ),
    path("activate/(<uib64>/(<token>/", Activate.as_view(), name="activate"),
    path("profile", Profile.as_view(), name="profile"),
    path("profile/edit/", EditProfile.as_view(), name="edit_profile"),
    path("", include("django.contrib.auth.urls")),
]
