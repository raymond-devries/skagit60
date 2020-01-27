from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


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
    climber = models.ForeignKey(User, on_delete=models.PROTECT)
    peak = models.ForeignKey(Peak, on_delete=models.PROTECT)
    date = models.DateField(help_text='The date you summited the peak.')

    def __str__(self):
        return self.climber.first_name + ' ' + self.climber.last_name + ', ' + str(self.peak)


@receiver(post_save, sender=Tick)
def mark_peak_as_complete(instance, created, **kwargs):
    if created:
        instance.peak.complete = True
        instance.peak.save()


@receiver(post_delete, sender=Tick)
def mark_peak_as_incomplete(sender, instance, **kwargs):
    if not sender.objects.filter(peak=instance.peak).exists():
        instance.peak.complete = False
        instance.peak.save()


class InterestedParticipant(models.Model):
    climber = models.ForeignKey(User, on_delete=models.CASCADE)
    peak = models.ForeignKey(Peak, on_delete=models.CASCADE)
    message = models.TextField(max_length=400)


class TripReport(models.Model):
    max_images = 4
    difficulty_choices = [
        (1, 'Easy'),
        (2, 'Moderate'),
        (3, 'Difficult'),
        (4, 'Epic')
    ]

    peak = models.ForeignKey(Peak, on_delete=models.PROTECT, null=True)
    published = models.BooleanField(default=False)
    writer = models.ForeignKey(User, on_delete=models.PROTECT)
    permits = models.CharField(null=True, blank=True, default=None, max_length=150)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    difficulty = models.IntegerField(choices=difficulty_choices, default=1)
    route_name = models.CharField(max_length=150, null=True, blank=True)
    snow_level = models.PositiveIntegerField(validators=[MaxValueValidator(15000)], null=True, blank=True)
    weather = models.TextField(null=True, blank=True)
    gear = models.TextField(null=True, blank=True)
    report = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.peak)


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


class ReportImage(models.Model):
    trip_report = models.ForeignKey(TripReport, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/trip_reports', null=True)


@receiver(pre_save, sender=ReportImage)
def image_validation(sender, instance, **kwargs):
    if sender.objects.filter(trip_report=instance.trip_report).count() >= TripReport.max_images:
        raise ValidationError('No more images allowed')
    if instance.image.size > 5242880:
        raise ValidationError('The image is more than 5mb')


class ReportComment(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()




