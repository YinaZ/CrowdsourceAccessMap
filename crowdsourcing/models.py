from djgeojson.fields import PolygonField
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    # USERNAME_FIELD = 'name'
class Data(models.Model):
    geom = PolygonField()
