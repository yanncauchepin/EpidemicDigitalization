from modules.places.data_places import DataPlaces
from modules.places.init_data_places import get_typage_place_from_osm_tags
from modules.roads.data_roads import DataRoads
from modules.tools.style import Color
import tqdm
import osmium
import pyproj
from shapely.geometry import Polygon
from shapely.ops import transform
from functools import partial
from math import floor


class OsmHandler (osmium.SimpleHandler) :

    def __init__(self, dataplace, dataroad) :
        osmium.SimpleHandler.__init__(self)
        self.__dataplace = dataplace
        self.__dataroad = dataroad
        self.__nodes = dict()
        self.__proj = partial(
            pyproj.transform, 
            pyproj.Proj('epsg:4326'),
            pyproj.Proj('epsg:3857')
            )
        print(f"{Color.CYAN}Extracting places and roads from osm file in "
              f"progress ...{Color.RESET}")


    def get_tags (self, tags) :
        osm_tags = dict()
        for tag in tags :
            osm_tags[tag.k] = tag.v
        return osm_tags


    def get_nodes_location(self, nodes) :
        list_nodes = list()
        for n in nodes :
            list_nodes.append(self.__nodes[n.ref])
        return list_nodes


    def get_area(self, nodes) :
        if (len(nodes) > 3) :
            coord = "["
            for i in range(len(nodes)-1) :
                coord += str(nodes[i]) + ","
            coord += str(nodes[-1]) + "]"
            p = Polygon(eval(coord))
            return floor(transform(self.__proj, p).area)
        else :
            return None


    def get_location(self, nodes) :
        sum_latitude = 0
        sum_longitude = 0
        for node in nodes :
            sum_latitude += node[0]
            sum_longitude += node[1]
        return (sum_latitude/len(nodes), sum_longitude/len(nodes))


    def node (self, n) :
        self.__nodes[n.id] = [n.location.lat, n.location.lon]
        
        
    def way (self, w) :
        osm_tags = self.get_tags(w.tags)
        type_name, subtype_name = get_typage_place_from_osm_tags(osm_tags)
        if type_name == 'data_road' and subtype_name == 'road' :
            nodes = self.get_nodes_location(w.nodes)
            id_key = w.id
            latitude, longitude = self.get_location(nodes)
            self.__dataroad.insert_road(
                id_key, 
                latitude, 
                longitude, 
                str(nodes), 
                str(osm_tags)
                )
        elif type_name != None and subtype_name != None :
            nodes = self.get_nodes_location(w.nodes)
            area = self.get_area(nodes)
            if (area != None) and (area>0):
                id_key = w.id
                latitude, longitude = self.get_location(nodes)
                self.__dataplace.insert_place(
                    id_key, 
                    type_name, 
                    subtype_name, 
                    latitude,
                    longitude,
                    area, 
                    str(nodes), 
                    str(osm_tags)
                    )
