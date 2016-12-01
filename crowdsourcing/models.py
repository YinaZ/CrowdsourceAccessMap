from djgeojson.fields import PolygonField
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.IntegerField()
    rank = models.IntegerField(default=0)


class Intersection(models.Model):
    geom = PolygonField()
    rank = models.IntegerField(default=0)


class Data(models.Model):
    geom = PolygonField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    intersection = models.ForeignKey(Intersection, on_delete=models.CASCADE)
