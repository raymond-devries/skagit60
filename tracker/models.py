from django.db import models
from users.models import Profile
from django.core.validators import MaxValueValidator


class Peak(models.Model):
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50, default=name)
    elevation = models.PositiveIntegerField()
    lat = models.DecimalField(decimal_places=5, max_digits=8)
    long = models.DecimalField(decimal_places=5, max_digits=8)
    peakbagger_link = models.URLField()
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tick(models.Model):
    climber = models.ForeignKey(Profile, on_delete=models.PROTECT)
    peak = models.ForeignKey(Peak, on_delete=models.PROTECT)


class PlannedTrip(models.Model):
    trip_leader = models.ForeignKey(Profile, on_delete=models.CASCADE)
    peak = models.ForeignKey(Peak, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    note = models.TextField()


class PlannedTripParticipant(models.Model):
    climber = models.ForeignKey(Profile, on_delete=models.CASCADE)
    planned_trip = models.ForeignKey(PlannedTrip, on_delete=models.CASCADE)
    message = models.TextField()


class TripReport(models.Model):
    difficulty_choices = [
        (1, 'Easy'),
        (2, 'Moderate'),
        (3, 'Difficult'),
        (4, 'Epic')
    ]

    peak = models.ForeignKey(Peak, on_delete=models.PROTECT)
    published = models.BooleanField(default=False)
    writer = models.ForeignKey(Profile, on_delete=models.PROTECT)
    permits = models.CharField(null=True, default=None, max_length=150)
    overnight = models.BooleanField(default=False)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)
    difficulty = models.IntegerField(choices=difficulty_choices, default=1)
    route_name = models.CharField(max_length=150, null=True)
    snow_level = models.PositiveIntegerField(validators=[MaxValueValidator(15000)], null=True)
    weather = models.TextField(null=True)
    gear = models.TextField(null=True)
    report = models.TextField(null=True)


class ReportTime(models.Model):
    points = [
        ('TH', 'Trail Head'),
        ('C', 'Camp'),
        ('S', 'Summit')
    ]
    trip_report = models.ForeignKey(TripReport, on_delete=models.CASCADE)
    start_point = models.CharField(max_length=30, choices=points)
    end_point = models.CharField(max_length=30, choices=points)
    time = models.DecimalField(decimal_places=1, max_digits=3)


class ReportComment(models.Model):
    user = models.ForeignKey(Profile, models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()




