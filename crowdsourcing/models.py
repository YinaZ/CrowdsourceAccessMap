from djgeojson.fields import PolygonField
from django.db import models

class Data(models.Model):
    geom = PolygonField()
