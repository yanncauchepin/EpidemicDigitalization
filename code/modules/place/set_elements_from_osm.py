import osmium
from Modules.Place import DataPlace, initDataPlace, DataRoad
import pyproj
from shapely.geometry import Polygon
from shapely.ops import transform
from functools import partial
from math import floor
from Modules.Tools.Style import color

class OsmHandler (osmium.SimpleHandler) :

    def __init__(self, network_file) :
        osmium.SimpleHandler.__init__(self)
        self.__dataroad = DataRoad.DataRoad(network_file)
        self.__nodes = dict()
        self.__proj = partial(pyproj.transform, pyproj.Proj('epsg:4326'),pyproj.Proj('epsg:3857'))
        self.__dataplace = DataPlace.DataPlace()
        self.__file = open("Modules/Place/PlacesFromOSM.txt", "w")
        print(f"{color.GREEN}Extracting places from osm file in progress ...{color.RESET}")

    def node (self, n) :
        self.__nodes[n.id] = [n.location.lat, n.location.lon]

    def getLocation(self, nodes) :
        sumlat = 0
        sumlon = 0
        for node in nodes :
            sumlat += node[0]
            sumlon += node[1]
        return (sumlat/len(nodes), sumlon/len(nodes))

    def getNodesLocation(self, nodes) :
        l = list()
        for n in nodes :
            l.append(self.__nodes[n.ref])
        return l

    def getArea(self, nodes) :
        if (len(nodes) > 3) :
            coord = "["
            for i in range(len(nodes)-1) :
                coord += str(nodes[i]) + ","
            coord += str(nodes[-1]) + "]"
            p = Polygon(eval(coord))
            return floor(transform(self.__proj, p).area)
        else :
            return None

    def getTags (self, tags) :
        osm_tags = dict()
        for tag in tags :
            osm_tags[tag.k] = tag.v
        return osm_tags

    def getPlaceType(self, osm_tags) :
        return initDataPlace.getTypePlaceFromOSM(osm_tags)

    def reportFile(self, id, type, subtype, location, area, nodes, osm_tags) :
        self.__file.write(f"""\n\n_________________________________________________________________
Way : {id}
    type : {type}
    subtype : {subtype}
    location : {location}
    area : {area}
    nodes : {nodes}
        """)
        for key, value in osm_tags.items() :
            self.__file.write("\t"*3 + f"osm_tags | {key} : {value}"+"\n")
        self.__file.write("_________________________________________________________________")


    def way (self, w) :
        osm_tags = self.getTags(w.tags)
        if osm_tags.get("highway") not in (None, "construction") :
            nodes = self.getNodesLocation(w.nodes)
            self.__dataroad.addRoad(id=w.id, location=self.getLocation(nodes), nodes=nodes, osm_tags=osm_tags)
        else :
            type, subtype = self.getPlaceType(osm_tags)
            if type != None and subtype != None :
                nodes = self.getNodesLocation(w.nodes)
                area = self.getArea(nodes)
                if (area != None) and (area >10) :
                    id = w.id
                    location = self.getLocation(nodes)
                    self.reportFile(id,type, subtype, location, area, nodes, osm_tags)
                    self.__dataplace.addPlace(id=id, location=location, type=type, subtype=subtype, area=area, nodes=nodes, osm_tags=osm_tags)
