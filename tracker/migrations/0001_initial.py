# Generated by Django 3.0.2 on 2020-01-09 21:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Peak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('elevation', models.PositiveIntegerField()),
                ('lat', models.DecimalField(decimal_places=5, max_digits=8)),
                ('long', models.DecimalField(decimal_places=5, max_digits=8)),
                ('peakbagger_link', models.URLField()),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PlannedTrip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('note', models.TextField()),
                ('peak', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tracker.Peak')),
                ('trip_leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='TripReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.BooleanField(default=False)),
                ('permits', models.CharField(default=None, max_length=150, null=True)),
                ('overnight', models.BooleanField(default=False)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('difficulty', models.IntegerField(choices=[(1, 'Easy'), (2, 'Moderate'), (3, 'Difficult'), (4, 'Epic')])),
                ('route_name', models.CharField(max_length=150, null=True)),
                ('snow_level', models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(15000)])),
                ('weather', models.TextField()),
                ('gear', models.TextField(null=True)),
                ('report', models.TextField(null=True)),
                ('peak', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tracker.Peak')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Tick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('climber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Profile')),
                ('peak', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tracker.Peak')),
            ],
        ),
        migrations.CreateModel(
            name='ReportTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_point', models.CharField(choices=[('TH', 'TrailHead'), ('C', 'Camp'), ('S', 'Summit')], max_length=30)),
                ('end_point', models.CharField(choices=[('TH', 'TrailHead'), ('C', 'Camp'), ('S', 'Summit')], max_length=30)),
                ('time', models.DecimalField(decimal_places=1, max_digits=3)),
                ('trip_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.TripReport')),
            ],
        ),
        migrations.CreateModel(
            name='ReportComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='PlannedTripParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('climber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
                ('planned_trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.PlannedTrip')),
            ],
        ),
    ]