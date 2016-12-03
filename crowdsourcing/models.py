from djgeojson.fields import GeometryField, GeometryCollectionField
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.IntegerField()
    rank = models.IntegerField(default=0)
    hr_rank = models.IntegerField(default=0)

class Intersection(models.Model):
    geom = GeometryField()
    rank = models.IntegerField(default=0)

class Data(models.Model):
    geom = GeometryField(default=None)
    sidewalks = models.TextField(default=None)
    correct = models.BooleanField(default=True)
    date = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    intersection = models.ForeignKey(Intersection, on_delete=models.CASCADE)
