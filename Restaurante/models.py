from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Keyword(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)
    website = models.CharField(max_length = 100)
    specific = models.CharField(max_length = 100)
    rating = models.FloatField(default=0.0)
    keywords = models.ManyToManyField(Keyword, related_name='Keywords')

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    favourites = models.ManyToManyField(Restaurant, related_name='Favourites')
    preferences = models.ManyToManyField(Keyword, related_name='Preferences')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
