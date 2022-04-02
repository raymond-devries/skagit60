from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View

from tracker.models import InterestedClimber, Tick, TripReport

from .forms import *
from .tokens import account_activation_token


class CustomLogin(LoginView):
    authentication_form = CustomAuthForm


class Signup(View):
    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return render(request, "registration/signup.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate Your Skagit60 Account"
            email_context = {
                "user": user,
                "protocol": request.scheme,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            }
            text_message = render_to_string("registration/account_activation_email.txt", email_context)
            html_message = render_to_string("registration/account_activation_email.html", email_context)
            user.email_user(subject, text_message, html_message=html_message)
            return redirect("account_activation_sent")

        else:
            return render(request, "registration/signup.html", {"form": form})


class AccountActivationSent(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration/account_activation_sent.html")


class Activate(View):
    def get(self, request, *args, **kwargs):
        uib64 = self.kwargs["uib64"]
        token = self.kwargs["token"]

        try:
            uid = force_str(urlsafe_base64_decode(uib64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(
                request,
                "Your account has been successfully been activated and you are now logged in.",
            )
            return redirect("home")
        else:
            messages.error(
                request,
                "We were unable to activate your account. You may have already activated your"
                "account. Please login. If you have any issues please contact"
                "skagitalpineclubwebsite@gmail.com",
            )
            return redirect("login")


class Profile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # since users can create trip reports without a peak associated,
        # they need to be deleted to avoid user confusion
        # a trip report filled in by the user will not contain a peak since it is a required field on the form
        self.delete_empty_trip_reports()
        ticks = Tick.objects.filter(climber=request.user)
        trip_reports = TripReport.objects.filter(writer=request.user)
        peak_interests = InterestedClimber.objects.filter(climber=request.user)
        return render(
            request,
            "users/profile.html",
            {
                "user": request.user,
                "ticks": ticks,
                "trip_reports": trip_reports,
                "peak_interests": peak_interests,
            },
        )

    def delete_empty_trip_reports(self):
        reports_to_delete = TripReport.objects.filter(writer=self.request.user, start=None)
        reports_to_delete.delete()


class EditProfile(LoginRequiredMixin, View):
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.request.user)
        return render(request, "users/edit_profile.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been updated.")
            return redirect("profile")

        else:
            return render(request, "users/edit_profile.html", {"form": form})
