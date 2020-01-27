from rest_framework.fields import CharField, ImageField, BooleanField
from rest_framework.serializers import ModelSerializer
from tracker.models import ReportTime, ReportImage, Tick, InterestedClimber


class ReportTimeSerializer(ModelSerializer):
    start_point_display = CharField(source='get_start_point_display', read_only=True)
    end_point_display = CharField(source='get_end_point_display', read_only=True)

    class Meta:
        model = ReportTime
        fields = '__all__'


class ReportImageSerializer(ModelSerializer):
    filepond = ImageField(source='image')

    class Meta:
        model = ReportImage
        fields = '__all__'


class TickSerializer(ModelSerializer):
    first_name = CharField(source='climber.first_name', read_only=True)
    last_name = CharField(source='climber.last_name', read_only=True)
    # This is returned to allow dynamic rendering of delete buttons when
    # the user adds a tick via the api on the peak detail page
    is_owner = BooleanField(default=True, read_only=True)

    class Meta:
        model = Tick
        fields = ['id', 'date', 'peak', 'first_name', 'last_name', 'is_owner']


class InterestedClimberSerializer(TickSerializer):
    class Meta:
        model = InterestedClimber
        fields = ['id', 'peak', 'first_name', 'last_name', 'is_owner']
