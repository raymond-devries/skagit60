from django.forms import ModelForm, DateField, DateInput, Textarea, CharField
from .models import TripReport, Tick


class TripReportForm(ModelForm):
    start = DateField(
        widget=DateInput(attrs={'type': 'date'}),
    )
    end = DateField(
        widget=DateInput(attrs={'type': 'date'}),
        required=False
    )
    weather = CharField(
        widget=Textarea(attrs={'rows': 3}),
        required=False
    )
    gear = CharField(
        widget=Textarea(attrs={'rows': 3}),
        required=False
    )

    class Meta:
        model = TripReport
        exclude = ['published', 'writer']


class CreateTickForm(ModelForm):
    date = DateField(
        widget=DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Tick
        exclude = ['climber']