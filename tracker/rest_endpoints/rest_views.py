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


class LinkedPeakPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.climber == request.user


class TickViewSet(ModelViewSet):
    queryset = Tick.objects.all()
    serializer_class = TickSerializer
    permission_classes = [LinkedPeakPermission]

    def perform_create(self, serializer):
        serializer.save(climber=self.request.user)


class InterestedClimberViewSet(TickViewSet):
    queryset = InterestedClimber.objects.all()
    serializer_class = InterestedClimberSerializer


class ReportCommentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ReportCommentViewSet(ModelViewSet):
    queryset = ReportComment.objects.all()
    serializer_class = ReportCommentSerializer
    permission_classes = [ReportCommentPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
