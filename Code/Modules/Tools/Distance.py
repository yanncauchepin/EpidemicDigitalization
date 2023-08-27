from shapely.geometry import LineString
import pyproj
from functools import partial
from shapely.ops import transform
from math import floor, sqrt, cos

def getShapeDistance(location1, location2):
    proj = partial(pyproj.transform, pyproj.Proj('epsg:4326'),pyproj.Proj('epsg:3857'))
    coord = "[" + str(location1) + "," + str(location2) + "]"
    line = transform(proj, LineString(eval(coord)))
    return floor(line.length)

def getMathDistance(location1, location2):
    #https://geodesie.ign.fr/contenu/fichiers/Distance_longitude_latitude.pdf
    lat1, lon1 = location1
    lat2, lon2 = location2
    lon1 = lon1*cos(floor(lat1)/90)
    lon2 = lon2*cos(floor(lat2)/90)
    return floor(sqrt((lat1-lat2)**2+(lon1-lon2)**2)*111110)
