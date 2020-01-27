from rest_framework.fields import CharField, ImageField
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from tracker.models import ReportTime, ReportImage


class ReportTimeSerializer(ModelSerializer):
    start_point_display = CharField(source='get_start_point_display', required=False)
    end_point_display = CharField(source='get_end_point_display', required=False)

    class Meta:
        model = ReportTime
        fields = '__all__'


class ReportImageSerializer(ModelSerializer):
    filepond = ImageField(source='image')

    class Meta:
        model = ReportImage
        fields = '__all__'
