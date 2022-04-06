from rest_framework.fields import CharField, ImageField
from rest_framework.serializers import ModelSerializer

from tracker.models import (
    InterestedClimber,
    ReportComment,
    ReportImage,
    ReportTime,
    Tick,
)


class ReportTimeSerializer(ModelSerializer):
    start_point_display = CharField(source="get_start_point_display", read_only=True)
    end_point_display = CharField(source="get_end_point_display", read_only=True)

    class Meta:
        model = ReportTime
        fields = "__all__"


class ReportImageSerializer(ModelSerializer):
    filepond = ImageField(source="image")

    class Meta:
        model = ReportImage
        fields = "__all__"


class TickSerializer(ModelSerializer):
    first_name = CharField(source="climber.first_name", read_only=True)
    last_name = CharField(source="climber.last_name", read_only=True)

    class Meta:
        model = Tick
        fields = ["id", "date", "peak", "first_name", "last_name"]


class InterestedClimberSerializer(TickSerializer):
    class Meta:
        model = InterestedClimber
        fields = ["id", "peak", "first_name", "last_name"]


class ReportCommentSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name", read_only=True)
    last_name = CharField(source="user.last_name", read_only=True)

    class Meta:
        model = ReportComment
        fields = ["id", "trip_report", "comment", "time", "first_name", "last_name"]
