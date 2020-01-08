from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class Peak(models.Model):
    name = models.CharField(max_length=50)
    elevation = models.PositiveIntegerField()
    lat = models.DecimalField(decimal_places=5, max_digits=8)
    long = models.DecimalField(decimal_places=5, max_digits=8)
    peakbagger_link = models.URLField()

    def __str__(self):
        return self.name


class TripReport(models.Model):
    difficulty_choices = [
        (1, 'Easy'),
        (2, 'Moderate'),
        (3, 'Difficult'),
        (4, 'Epic')
    ]

    peak = models.ForeignKey(Peak, on_delete=models.PROTECT)
    climber = models.ForeignKey(User, on_delete=models.PROTECT)
    start = models.DateTimeField()
    end = models.DateTimeField()
    difficulty = models.IntegerField(choices=difficulty_choices)
    route_name = models.CharField(max_length=150, null=True)
    snow_level = models.PositiveIntegerField(validators=[MaxValueValidator(15000)], null=True)
    weather = models.TextField()
    equipment = models.TextField(null=True)
    report = models.TextField(null=True)


class Climbers(models.Model):
    climber = models.ForeignKey(User, on_delete=models.PROTECT)
    report = models.ForeignKey(TripReport, on_delete=models.CASCADE)
