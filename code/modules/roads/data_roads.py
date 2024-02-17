from modules.tools.singleton import Singleton
from modules.tools.distance import get_custom_distance, get_shapely_distance
from modules.tools.style import Color
from modules.places.data_places import Place
import os
import sumolib
from tqdm import tqdm
import sqlite3


def assign_road_place(dataplaces, dataroads) :

    print(f"{Color.CYAN}Assigning a road to each places in progress ..."
          f"{Color.RESET}")
    all_places = dataplaces.get_all_places()
    with tqdm(total=len(all_places), desc="Assigning roads") as pbar:
        for place in all_places:
            place_latitude = Place(place)['latitude']
            place_longitude = Place(place)['longitude']
            place_id = Place(place)['id']
            road = dataroads.get_nearest_road(place_latitude, place_longitude)
            road_id = Road(road)['id']
            dataplaces.assign_road_id_to_place(place_id, road_id)
            pbar.update(1)


class Road():
    
    def __init__(self, road):
        self.road = road
        
    def __getitem__(self, key):
        values = {
            'id' : self.road[0],
            'sumomobility_id' : self.road[1],
            'latitude' : self.road[2],
            'longitude' : self.road[3],
            'location' : [self.road[2], self.road[3]],
            'nodes' : eval(self.road[4]),
            'tags' : eval(self.road[5])
            }
        if key in values.keys():
            return values[key]
        elif key in ['all', 'values']:
            return values
        else:
            raise KeyError(f"Key '{key}' not found.")


class DataRoads(metaclass=Singleton):
    
    '''
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

    '''
    '''
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
    '''
    __sumomobility_network_initialized = False
    __sumomobility_id = list()
    
    def __init__(self, database_path, sumomobility_network_path=None, 
                 raise_error_on_duplicate_id=False,
                 raise_warning_not_related_sumomobility_edges=False) :
        if self.__sumomobility_network_initialized == False:
            if sumomobility_network_path == None or not os.path.exists(sumomobility_network_path):
                raise ValueError(f'DataRoads bust me initialized in the first init '
                                 'with a valid sumomobility_network_path.')
            else :
                self.__init_sumomobility_edges(sumomobility_network_path)
                __sumomobility_network_initialized = True
        os.makedirs(os.path.dirname(database_path), exist_ok=True) 
        self.database_path = database_path
        self.raise_error_on_duplicate_id = raise_error_on_duplicate_id
        self.raise_warning_not_related_sumomobility_edges = raise_warning_not_related_sumomobility_edges
        
    def __init_sumomobility_edges(self, sumomobility_network_path) :
        net = sumolib.net.readNet(sumomobility_network_path)
        sumo_edges = net.getEdges()
        for elem in sumo_edges :
            self.__sumomobility_id.append(elem.getID())
        return True
    
    def __get_sumomobility_id_from_osm_id(self, osm_id) :
        available_id = list([f'{osm_id}',f'{osm_id}#0',f'{osm_id}#1',f'{osm_id}#2', 
                             f'{osm_id}#3', f'{osm_id}#4'])
        find = None
        i = 0
        while find == None and i < len(available_id) :
            if available_id[i] in self.__sumomobility_id :
                find = available_id[i]
            i += 1
        return find
        
    def __start_connection_db(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        
    def __end_connection_db(self):
        self.cursor.close()
        self.connection.close()
    
    def create_database(self) :
        self.__start_connection_db()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Roads (
            id INTEGER PRIMARY KEY, 
            sumomobility_id TEXT,
            latitude REAL,
            longitude REAL,
            nodes TEXT,
            tags TEXT
            )''')
        self.__end_connection_db()
        
    def insert_road(self, id_key, latitude, longitude, nodes="None", tags="None"):
        self.__start_connection_db()
        # Check if the id_key already exists
        self.cursor.execute("SELECT id FROM Roads WHERE id = ?", 
                            (id_key,))
        existing_id = self.cursor.fetchone()
        if existing_id:
            if self.raise_error_on_duplicate_id:
                raise ValueError(f"ID {id_key} already exists in the roads "
                                 "database.\n")
            else:
                print(f"{Color.RED}Warning:{Color.RESET} id {id_key} already "
                      "exists in the roads database.\n")
        else:
            sumomobility_id = self.__get_sumomobility_id_from_osm_id(id_key)
            if sumomobility_id == None:
                if self.raise_warning_not_related_sumomobility_edges :
                    print(f"{Color.RED}Warning:{Color.RESET} Osm road id {id_key} "
                          "can not be related to any sumomobility edges id.")
                sumomobility_id = str(sumomobility_id)
            # Insert the road
            self.cursor.execute('''INSERT INTO Roads (
                id, sumomobility_id, latitude, longitude, nodes, tags
                ) VALUES (?, ?, ?, ?, ?, ?)''',
            (id_key, sumomobility_id, latitude, longitude, nodes, tags))
            self.connection.commit()
        self.__end_connection_db()

    def remove_road(self, id_key):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM Roads WHERE id = ?", 
                            (id_key,))
        self.connection.commit()
        self.__end_connection_db()
        
    def reset_database(self):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM Roads")
        self.connection.commit()
        self.__end_connection_db()

    """Get roads"""
    
    def get_all_roads(self) :
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Roads")
        all_roads = self.cursor.fetchall()
        self.__end_connection_db()
        return all_roads
    
    def get_id_road(self, id_key):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Roads WHERE id = ? ", 
                            (id_key,))
        id_road = self.cursor.fetchall()
        self.__end_connection_db()
        return id_road
    
    """List ids"""
    
    def list_all_ids(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT id FROM Roads")
        all_ids = [row[0] for row in self.cursor.fetchall()]
        self.__end_connection_db()
        return all_ids

    """Count places"""

    def count_roads(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM Roads")
        count_all = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_all
    
    """Get nearest road from location"""

    def get_nearest_road(self, latitude, longitude):
        all_roads = self.get_all_roads()
        # Define a filter to gradually increase the search radius
        filter_value = 1e-3
        # Search for the nearest road
        search = True
        while search:
            neighbors = []
            # Iterate over each road
            for road in all_roads:
                road_latitude = Road(road)['latitude']
                road_longitude = Road(road)['longitude']
                # Check if the road is within the filter range
                if abs(road_latitude - latitude) < filter_value and \
                abs(road_longitude - longitude) < filter_value:
                    neighbors.append(road)
            # If there are neighbors, find the closest road
            if neighbors:
                best_road = neighbors[0]
                best_distance = get_shapely_distance((road_latitude, road_longitude), (latitude, longitude))
                for road in neighbors[1:]:
                    distance = get_shapely_distance((road_latitude, road_longitude), (latitude, longitude))
                    if distance < best_distance:
                        best_road = road
                        best_distance = distance
                search = False
            else : # If no neighbors are found within the current filter range, increase the filter value
                filter_value += 1e-3
        return best_road
    
    
    def get_nearest_road_deprecated(self, latitude, longitude):
        best_road = None
        best_distance = float('inf')
        for road in self.get_all_roads():
            road_latitude = Road(road)["latitude"]
            road_longitude = Road(road)["longitude"]
            distance = get_shapely_distance(
                (road_latitude, road_latitude),
                (latitude, longitude)
                )
            if distance < best_distance:
                best_road = road
                best_distance = distance
        return best_road
    

'''----------------------------------------------------------------> DEPRECATED
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
'''