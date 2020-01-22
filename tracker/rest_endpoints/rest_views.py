from rest_framework.viewsets import ModelViewSet
from .serializers import *


class ReportTimeViewSet(ModelViewSet):
    queryset = ReportTime.objects.all()
    serializer_class = ReportTimeSerializer
