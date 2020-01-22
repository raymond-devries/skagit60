from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField
from tracker.models import ReportTime


class ReportTimeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ReportTime
        fields = '__all__'
