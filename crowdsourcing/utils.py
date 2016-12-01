from .settings import MEDIA_ROOT
from .models import Intersection
import csv

def get_intersection():
    csv_file_name = '/intersection.csv'
    path = MEDIA_ROOT + csv_file_name
    with open(path) as intersections:
        read_csv = csv.reader(intersections, delimiter=',')
        for row in read_csv:
            if (row[0] == 'lat'):
                continue
            intersection = Intersection()
            geom = {'type': 'Point', 'coordinates': [row[1], row[0]]}
            intersection.geom = geom
            intersection.rank = row[2]
            intersection.save()
