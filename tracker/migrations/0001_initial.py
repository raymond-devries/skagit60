# Generated by Django 4.0.3 on 2022-04-02 01:23

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Peak",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("display_name", models.CharField(default=models.CharField(max_length=50), max_length=50)),
                ("elevation", models.PositiveIntegerField()),
                ("lat", models.DecimalField(decimal_places=5, max_digits=8)),
                ("long", models.DecimalField(decimal_places=5, max_digits=8)),
                ("peakbagger_link", models.URLField()),
                ("complete", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="TripReport",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("published", models.BooleanField(default=False)),
                ("permits", models.CharField(blank=True, default=None, max_length=150, null=True)),
                ("start", models.DateField(blank=True, null=True)),
                ("end", models.DateField(blank=True, null=True)),
                (
                    "difficulty",
                    models.IntegerField(
                        choices=[(1, "Easy"), (2, "Moderate"), (3, "Difficult"), (4, "Epic")], default=1
                    ),
                ),
                ("route_name", models.CharField(blank=True, max_length=150, null=True)),
                (
                    "snow_level",
                    models.PositiveIntegerField(
                        blank=True, null=True, validators=[django.core.validators.MaxValueValidator(15000)]
                    ),
                ),
                (
                    "elevation_gain",
                    models.PositiveIntegerField(
                        blank=True, null=True, validators=[django.core.validators.MaxValueValidator(15000)]
                    ),
                ),
                ("total_miles", models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ("weather", models.TextField(blank=True, null=True)),
                ("gear", models.TextField(blank=True, null=True)),
                ("report", models.TextField(blank=True, null=True)),
                ("peak", models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to="tracker.peak")),
                ("writer", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Tick",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(help_text="The date you summited the peak.")),
                (
                    "climber",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
                ),
                ("peak", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tracker.peak")),
            ],
        ),
        migrations.CreateModel(
            name="ReportTime",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "start_point",
                    models.CharField(choices=[("TH", "Trail Head"), ("C", "Camp"), ("S", "Summit")], max_length=30),
                ),
                (
                    "end_point",
                    models.CharField(choices=[("TH", "Trail Head"), ("C", "Camp"), ("S", "Summit")], max_length=30),
                ),
                ("time", models.DecimalField(decimal_places=1, max_digits=3)),
                (
                    "trip_report",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tracker.tripreport"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReportImage",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(null=True, upload_to="images/trip_reports")),
                (
                    "trip_report",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tracker.tripreport"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReportComment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("time", models.DateTimeField(auto_now_add=True)),
                ("comment", models.TextField()),
                (
                    "trip_report",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tracker.tripreport"),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="InterestedClimber",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "climber",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
                ("peak", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tracker.peak")),
            ],
        ),
    ]
