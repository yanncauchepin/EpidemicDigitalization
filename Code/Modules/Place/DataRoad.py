import os
import sys
from Modules.Tools.Style import color

if 'SUMO_HOME' in os.environ :
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else :
    sys.exit(f"{color.RED}Please declare environment variable {color.BLUE}'SUMO_HOME'{color.RESET}")

import sumolib
from random import sample
from Modules.Tools import Singleton
from Modules.Tools.Distance import getMathDistance

class DataRoad (metaclass=Singleton.Singleton) :
    __network_file_check = False

    def __init__(self, network_file=None) :
        self.__road = dict()
        self.__sumo = list()
        if self.__network_file_check == False :
            if network_file == None :
                print(f"{color.RED}Error :{color.RESET} For the first call of DataRoad you must give {color.BLUE}network_file{color.RESET} in parameter")
            else :
                valid = self.__initSumoEdges(network_file)
                if valid == True :
                    self.__network_file_check = True


    def __initSumoEdges(self, network_file) :
        net = sumolib.net.readNet(network_file)
        sumo_edges = net.getEdges()
        for elem in sumo_edges :
            self.__sumo.append(elem.getID())
        return True

    def getRoads (self) :
        l = list()
        for key in self.__road.keys() :
            l.append(key)
        return l

    def getRoad (self, road) :
        road = str(road)
        if road not in self.getRoads() :
            print(f"{color.RED}Error :{color.RESET} Road {color.BLUE}{road}{color.RESET} is not in DataRoad")
        else :
            return self.__road[road]

    def getSumo (self) :
        return self.__sumo

    def addRoad(self, id, location, nodes, **kwargs) :
        sumo_id = self.__getSumoIdFromOsmId(id)
        if sumo_id != None :
            sumo_id = str(sumo_id)
            if sumo_id in self.getRoads() :
                print(f"{color.RED}Error :{color.RESET} Road {color.BLUE}{sumo_id}{color.RESET} is already in DataRoad")
            else :
                self.__road[sumo_id] = self.Road(id, location, nodes, **kwargs)
        else :
            print(f"{color.RED}Error :{color.RESET} Id {color.BLUE}{id}{color.RESET} from {color.CYAN}OSM{color.RESET} cannot be linked to a {color.CYAN}SUMO Edge{color.RESET}")

    def __getSumoIdFromOsmId(self, osm_id) :
        id = list([str(osm_id),str(osm_id)+"#0",str(osm_id)+"#1",str(osm_id)+"#2"])
        find = None
        i = 0
        while find == None and i < 4 :
            if id[i] in self.getSumo() :
                find = id[i]
            i += 1
        if find != None :
            return find
        else :
            return None

    def getNearestRoad(self, location) :
        if len(self.getRoads()) == 0 :
            print(f"{color.RED}Error :{color.RESET} No roads in DataRoad")
            return None
        else :
            filter = 1e-3
            neighbors = list()
            best = None
            while len(neighbors) == 0 :
                for road in self.getRoads() :
                    road_location = self.getRoad(road).getLocation()
                    if abs(road_location[0] - location[0]) < filter and abs(road_location[1] - location[1]) < filter :
                        neighbors.append(road)
                filter += 1e-3
            best = neighbors[0]
            best_score = getMathDistance(self.getRoad(best).getLocation(), location)
            if len(neighbors) > 1 :
                for road in neighbors[1:] :
                    distance = getMathDistance(self.getRoad(road).getLocation(), location)
                    if distance < best_score :
                        best = road
                        best_score = distance
            return best

    def __str__(self, **kwargs) :
        kwargs = dict()
        kwargs["indent"] = 1
        limit = kwargs.get("limit", 30)

        string = f"{color.UNDERLINE}Roads :{color.RESET}"
        roads = self.getRoads()
        if len(roads) > 0 :
            if len(roads) < limit or limit == None :
                size = len(roads)
            else :
                size = limit
            r = sample(roads, size)
            for id in r :
                string += f"\n\n{self.getRoad(id).__str__(**kwargs)}"
            if len(people) > limit :
                string += "\n\t\t" + "\t"*indent + f"{color.BLUE}...{color.RESET}"
        return string

    def __repr__(self) :
        return self.__str__()

    class Road () :
        def __init__(self, id, location, nodes, **kwargs) :
            self.__id = id
            self.__location = location
            self.__nodes = nodes
            self.__osm_tags = kwargs.get("osm_tags", None)
            self.__places = list()

        def getId (self) :
            return self.__id

        def getLocation (self) :
            return self.__location

        def getOsmTags (self) :
            return self.__osm_tags

        def getPlaces (self) :
            return self.__places

        def addPlace (self, place) :
            if place in self.getPlaces() :
                self.__places.append(place)
            else :
                print(f"{color.RED}Error :{color.RESET} Place {color.BLUE}{place}{color.RESET} is already linked to road {self.getId()}")

        def removePlace (self, place) :
            if place in self.getPlaces() :
                self.__places.remove(place)
            else :
                print(f"{color.RED}Error :{color.RESET} Place {color.BLUE}{place}{color.RESET} is not linked to road {self.getId()}")

        def __str__(self, **kwargs) :
            indent = kwargs.get("indent", 0)

            string = "\t"*indent + f"{color.UNDERLINE}Road :{color.BLUE}{self.getId()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"location : {color.CYAN}{self.getLocation()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"nodes : {color.CYAN}{self.getNodes()}{color.RESET}"
            osm_tags = self.getOsmTags()
            if osm_tags != None :
                string += "\n\t" + "\t"*indent + "Osm tags :"
                for key, value in osm_tags.items() :
                    string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{key}{color.RESET} : {value}"
            places = self.getPlaces()
            if len(places) > 0 :
                string += "\n\t" + "\t"*indent + "Places :"
                for place in self.getPlaces() :
                    string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{place}{color.RESET}"
            return string

        def __repr__(self) :
            return self.__str__()
