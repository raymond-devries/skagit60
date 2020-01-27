from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.permissions import BasePermission


class LinkedTripReportPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.trip_report.writer == request.user


class ReportTimeViewSet(ModelViewSet):
    queryset = ReportTime.objects.all()
    serializer_class = ReportTimeSerializer
    permission_classes = [LinkedTripReportPermission]


class ReportImageViewSet(ModelViewSet):
    queryset = ReportImage.objects.all()
    serializer_class = ReportImageSerializer
    permission_classes = [LinkedTripReportPermission]


class TickViewSet(ModelViewSet):
    queryset = Tick.objects.all()
    serializer_class = TickSerializer

    def perform_create(self, serializer):
        serializer.save(climber=self.request.user)
