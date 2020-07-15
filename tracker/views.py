from django.db.models import Count, Min
from skagit60 import settings
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    View,
    TemplateView,
)
from tracker.models import *
from .forms import *
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
import subprocess
import os


class Home(View):
    def get(self, request, *args, **kwargs):
        context = {
            "peaks": serializers.serialize(
                "json", Peak.objects.annotate(tick_date=Min("tick__date"))
            ),
            "number_of_peaks_completed": Peak.objects.filter(complete=True).count(),
        }
        return render(request, "tracker/home.html", context)


class About(TemplateView):
    template_name = "tracker/about.html"


class PeakDetail(DetailView):
    model = Peak

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticks"] = self.get_ticks_json()
        context["interested_climbers"] = self.get_interested_climbers_json()
        context["reports"] = TripReport.objects.filter(
            peak=self.get_object(), published=True
        )
        return context

    def get_interested_climbers_json(self):
        interested_climbers = InterestedClimber.objects.filter(
            peak=self.get_object()
        ).order_by("climber__first_name")
        interested_climbers_list = []
        for climber in interested_climbers:
            interested_climbers_list.append(
                {
                    "id": climber.id,
                    "first_name": climber.climber.first_name,
                    "last_name": climber.climber.last_name,
                    "is_owner": climber.climber == self.request.user,
                }
            )
        interested_climbers_json = json.dumps(interested_climbers_list)
        return interested_climbers_json

    def get_ticks_json(self):
        ticks = Tick.objects.filter(peak=self.get_object()).order_by("-date")
        ticks_dict = []
        for tick in ticks:
            ticks_dict.append(
                {
                    "id": tick.id,
                    "date": tick.date.strftime(settings.REST_FRAMEWORK["DATE_FORMAT"]),
                    "first_name": tick.climber.first_name,
                    "last_name": tick.climber.last_name,
                    "is_owner": tick.climber == self.request.user,
                }
            )
        ticks_json = json.dumps(ticks_dict)
        return ticks_json


class TripReportDetail(DetailView):
    model = TripReport
    queryset = model.objects.filter(published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.get_object()
        context["show_end"] = report.start != report.end and report.end is not None
        context["images"] = ReportImage.objects.filter(trip_report=report)
        context["times"] = ReportTime.objects.filter(trip_report=report)
        context["comments"] = self.get_comments_json(report)

        return context

    def get_comments_json(self, report):
        comments = ReportComment.objects.filter(trip_report=report).order_by("-time")
        comments_list = []
        for comment in comments:
            comments_list.append(
                {
                    "id": comment.id,
                    "comment": comment.comment,
                    "time": comment.time.strftime(
                        settings.REST_FRAMEWORK["DATETIME_FORMAT"]
                    ),
                    "first_name": comment.user.first_name,
                    "last_name": comment.user.last_name,
                    "is_owner": comment.user == self.request.user,
                }
            )
        comments_json = json.dumps(comments_list)

        return comments_json


class TripReportCreate(LoginRequiredMixin, View):
    form_class = TripReportForm

    def get(self, request, *args, **kwargs):
        # an instance must be created to ensure that apis that add related models will work during trip report creation
        user = self.request.user
        try:
            try:
                peak = Peak.objects.get(id=self.kwargs["peak_id"])
            except Peak.DoesNotExist:
                raise Http404
            trip_report = TripReport(writer=user, peak=peak)
            trip_report.save()
        except KeyError:
            trip_report = TripReport(writer=user)
            trip_report.save()
        return redirect("trip_report_update", pk=trip_report.pk)


class TripReportUpdate(LoginRequiredMixin, UpdateView):
    model = TripReport
    form_class = TripReportForm
    success_url = reverse_lazy("profile")

    def get_queryset(self):
        return TripReport.objects.filter(pk=self.kwargs["pk"], writer=self.request.user)

    def form_valid(self, form):
        trip_report = form.save(commit=False)
        if "publish_report" in self.request.POST:
            trip_report.published = True
        trip_report.save()
        return redirect("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.get_object()
        context["times"] = self.get_report_times_json(report)
        context["time_choices"] = json.dumps(
            ReportTime._meta.get_field("start_point").choices
        )

        images, images_json = self.get_images(report)
        context["images"] = images_json
        context["max_uploads"] = TripReport.max_images - images.count()

        return context

    @staticmethod
    def get_images(report):
        images = ReportImage.objects.filter(trip_report=report)
        images_dict = {}
        for image in images:
            images_dict[image.id] = {"id": image.id, "url": image.image.url}
        images_json = json.dumps(images_dict)
        return images, images_json

    @staticmethod
    def get_report_times_json(report):
        times = ReportTime.objects.filter(trip_report=report)
        times_dict = {}
        for time in times:
            times_dict[time.id] = {
                "start_point_display": time.get_start_point_display(),
                "end_point_display": time.get_end_point_display(),
                "time": str(time.time),
                "id": time.id,
            }
        times_json = json.dumps(times_dict)
        return times_json


class TripReportDelete(LoginRequiredMixin, DeleteView):
    model = TripReport
    success_url = reverse_lazy("profile")

    def get_queryset(self):
        return TripReport.objects.filter(pk=self.kwargs["pk"], writer=self.request.user)


class LeaderBoard(View):
    def get(self, request, *args, **kwargs):
        leaders = (
            User.objects.annotate(num_of_peaks=Count("tick__peak", distinct=True))
            .filter(num_of_peaks__gt=0)
            .order_by("-num_of_peaks")
        )
        return render(request, "tracker/leaderboard.html", {"leaders": leaders})


class TripReports(ListView):
    model = TripReport
    template_name = "tracker/trip_reports.html"
    context_object_name = "trip_reports"
    queryset = TripReport.objects.filter(published=True).order_by("-start")


class LoaderVerification(View):
    def get(self, request, *args, **kwargs):
        context = {"token": settings.LOADER_VERIFICATION_TOKEN}
        return render(request, "tracker/loader_verification.html", context)


@method_decorator(staff_member_required, name="dispatch")
class Status(View):
    def get(self, request, *args, **kwargs):
        current_directory = os.getcwd()
        command = (
            f"goaccess {current_directory}/nginx/logs/access.log -a -o "
            f"{current_directory}/templates/report.html --log-format=COMBINED"
        )
        subprocess.run(command, shell=True)
        html_file_path = f"{current_directory}/templates/report.html"
        with open(html_file_path) as file:
            html = file.read()
        return HttpResponse(html)
