from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from tracker.models import *


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


