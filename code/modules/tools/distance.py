from shapely.geometry import LineString
import pyproj
from functools import partial
from shapely.ops import transform
from math import floor, radians, sin, cos, acos

def get_shape_distance(location1, location2):
    proj = partial(pyproj.transform, pyproj.Proj('epsg:4326'),pyproj.Proj('epsg:3857'))
    coord = "[" + str(location1) + "," + str(location2) + "]"
    line = transform(proj, LineString(eval(coord)))
    return floor(line.length)

def get_math_distance(location1, location2):
    #https://geodesie.ign.fr/contenu/fichiers/Distance_longitude_latitude.pdf
    lat1, lon1 = map(radians, location1)
    lat2, lon2 = map(radians, location2)
    distance = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * 6371000
    # 6371 is the mean radius of the Earth in meters
    return distance
