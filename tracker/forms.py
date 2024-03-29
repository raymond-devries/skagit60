from django.forms import CharField, DateField, DateInput, ModelForm, Textarea

from .models import TripReport


class TripReportForm(ModelForm):
    start = DateField(widget=DateInput(attrs={"type": "date"}))
    end = DateField(widget=DateInput(attrs={"type": "date"}), required=False)
    weather = CharField(widget=Textarea(attrs={"rows": 3}), required=False)
    gear = CharField(widget=Textarea(attrs={"rows": 3}), required=False)

    class Meta:
        model = TripReport
        exclude = ["published", "writer"]
