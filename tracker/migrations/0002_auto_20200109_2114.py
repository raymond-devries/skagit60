# Generated by Django 3.0.2 on 2020-01-09 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporttime',
            name='end_point',
            field=models.CharField(choices=[('TH', 'Trail Head'), ('C', 'Camp'), ('S', 'Summit')], max_length=30),
        ),
        migrations.AlterField(
            model_name='reporttime',
            name='start_point',
            field=models.CharField(choices=[('TH', 'Trail Head'), ('C', 'Camp'), ('S', 'Summit')], max_length=30),
        ),
        migrations.AlterField(
            model_name='tripreport',
            name='difficulty',
            field=models.IntegerField(choices=[(1, 'Easy'), (2, 'Moderate'), (3, 'Difficult'), (4, 'Epic')], default=1),
        ),
        migrations.AlterField(
            model_name='tripreport',
            name='end',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tripreport',
            name='start',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tripreport',
            name='weather',
            field=models.TextField(null=True),
        ),
    ]
