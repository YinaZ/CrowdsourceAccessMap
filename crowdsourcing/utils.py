from .settings import MEDIA_ROOT
from .models import Intersection, ItrCsvModel

def get_intersection():
    csv_file_name = '/intersection.csv'
    path = MEDIA_ROOT + csv_file_name
    itr_csv_list = ItrCsvModel.import_data(data = open(path))

    for coordinate in itr_csv_list:
        print "lat: " + str(coordinate.lat) + ", lon:  " + str(coordinate.lon) + ", score: " + str(coordinate.score)
        geom = {'type': 'Point', 'coordinates': [coordinate.lat, coordinate.lon]}
        intersection = Intersection()
        intersection.geom = geom
        intersection.save()
