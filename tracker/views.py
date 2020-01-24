from django.contrib import messages
from django.core import serializers
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, DeleteView, UpdateView, View
from tracker.models import *
from .forms import *


class Home(ListView):
    model = Peak
    template_name = 'tracker/home.html'
    context_object_name = 'peaks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_of_peaks_completed'] = Peak.objects.filter(complete=True).count()
        return context


class PeakDetail(DetailView):
    model = Peak

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticks'] = Tick.objects.filter(peak=self.get_object())
        context['reports'] = TripReport.objects.filter(peak=self.get_object())
        return context


class TripReportDetail(DetailView):
    model = TripReport

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.get_object()
        try:
            context['show_end'] = report.start != report.end
        except AttributeError:
            # if end date or start date is none, an attribute error is thrown
            context['show_end'] = False

        context['times'] = ReportTime.objects.filter(trip_report=report)

        return context


class TripReportCreate(LoginRequiredMixin, View):
    form_class = TripReportForm

    def get(self, request, *args, **kwargs):
        # an instance must be created to ensure that apis that add related models will work during trip report creation
        user = self.request.user
        trip_report = TripReport(writer=user)
        trip_report.save()
        return redirect('trip_report_update', pk=trip_report.pk)


class TripReportUpdate(LoginRequiredMixin, UpdateView):
    model = TripReport
    form_class = TripReportForm
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return TripReport.objects.filter(pk=self.kwargs['pk'], writer=self.request.user)

    def form_valid(self, form):
        trip_report = form.save(commit=False)
        if 'publish_report' in self.request.POST:
            trip_report.published = True
        trip_report.save()
        return redirect('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.get_object()
        times = ReportTime.objects.filter(trip_report=report)
        times_dict = {}
        for time in times:
            times_dict[time.id] = \
                {'start_point_display': time.get_start_point_display(),
                 'end_point_display': time.get_end_point_display(),
                 'time': str(time.time),
                 'id': time.id}
        
        context['times'] = json.dumps(times_dict)
        context['time_choices'] = json.dumps(ReportTime._meta.get_field('start_point').choices)

        return context


class TripReportDelete(LoginRequiredMixin, DeleteView):
    model = TripReport
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return TripReport.objects.filter(pk=self.kwargs['pk'], writer=self.request.user)


class TickCreate(LoginRequiredMixin, FormView):
    form_class = CreateTickForm
    template_name = 'tracker/tick_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.climber = self.request.user
        form.save()
        return super().form_valid(form)


class TickDelete(LoginRequiredMixin, DeleteView):
    model = Tick
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return Tick.objects.filter(pk=self.kwargs['pk'], climber=self.request.user)
