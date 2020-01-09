from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, models.PROTECT)
    active = models.BooleanField(default=True)
