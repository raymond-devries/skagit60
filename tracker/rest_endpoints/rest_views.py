from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from .serializers import *


class ReportTimeViewSet(ModelViewSet):
    queryset = ReportTime.objects.all()
    serializer_class = ReportTimeSerializer


class ReportImageViewSet(ModelViewSet):
    parser_classes = [MultiPartParser]
    queryset = ReportImage.objects.all()
    serializer_class = ReportImageSerializer

