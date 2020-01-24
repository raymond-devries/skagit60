from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from tracker.models import ReportTime, ReportImage


class ReportTimeSerializer(ModelSerializer):
    start_point_display = CharField(source='get_start_point_display', required=False)
    end_point_display = CharField(source='get_end_point_display', required=False)

    class Meta:
        model = ReportTime
        fields = '__all__'


class ReportImageSerializer(ModelSerializer):
    class Meta:
        model = ReportImage
        fields = '__all__'
