from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save


# Create your models here.

class Keyword(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)
    website = models.CharField(max_length = 100)
    rating = models.FloatField(default=0.0)
    keywords = models.ManyToManyField(Keyword, related_name='Keywords')

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    birth_date = models.DateField(null=True, blank=True)
    #favourites = models.ManyToManyField(Restaurant, related_name='Favourites')
    preferences = models.ManyToManyField(Keyword, related_name='Preferences')
    trained = models.BooleanField(blank=True, default=False)
    #artificial_id = models.IntegerField(blank=True, default=-1)
    email_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
