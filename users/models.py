from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ValidEmail(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
