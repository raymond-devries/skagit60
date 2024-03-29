import json
import os
import subprocess

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Count, F, Min
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from skagit60 import settings
from tracker.models import *

from .forms import *


class Home(View):
    def get(self, request, *args, **kwargs):
        all_peaks = Peak.objects.all()
        completed_peaks = Peak.objects.filter(complete=True)
        incomplete_peaks = Peak.objects.filter(complete=False)
        most_recently_completed = Peak.objects.annotate(date=Min("tick__date")).filter(complete=True).order_by("-date")

        context = {
            "all_peaks": self.get_peaks_json(request, all_peaks),
            "complete_peaks": self.get_peaks_json(request, completed_peaks),
            "incomplete_peaks": self.get_peaks_json(request, incomplete_peaks),
            "most_recently_completed": self.get_peaks_json(request, most_recently_completed),
            "number_of_peaks_completed": completed_peaks.count(),
        }
        return render(request, "tracker/home.html", context)

    def get_peaks_json(self, request, query):
        peaks = query
        info = [
            {
                "url": request.build_absolute_uri(reverse("peak_detail", kwargs={"pk": peak.pk})),
                "pk": peak.pk,
                "name": peak.name,
                "complete": peak.complete,
            }
            for peak in peaks
        ]
        peaks_json = json.dumps(info)
        return peaks_json


class About(TemplateView):
    template_name = "tracker/about.html"


class PeakDetail(DetailView):
    model = Peak

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticks"] = self.get_ticks_json()
        context["interested_climbers"] = self.get_interested_climbers_json()
        context["reports"] = TripReport.objects.filter(peak=self.get_object(), published=True)
        return context

    def get_interested_climbers_json(self):
        interested_climbers = InterestedClimber.objects.filter(peak=self.get_object()).order_by("climber__first_name")
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
                    "time": comment.time.strftime(settings.REST_FRAMEWORK["DATETIME_FORMAT"]),
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
        context["time_choices"] = json.dumps(ReportTime._meta.get_field("start_point").choices)

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
