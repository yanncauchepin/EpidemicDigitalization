from modules.place.data_place import DataPlace
from modules.tools.style import Color
#, initDataPlace, DataRoad
import osmium
import pyproj
from shapely.geometry import Polygon
from shapely.ops import transform
from functools import partial
from math import floor

def get_typage_place_from_osm_tags(osm_tags) :

    #Type : accomodation
    if (osm_tags.get("building") == "hotel") \
    or (osm_tags.get("tourism") in ("hotel", "apartment", "motel", "guest_home")) :
        return ("accomodation", "hotel")
    elif (osm_tags.get("building") in ("apartments", "detached", "house", "residential", "semidetached_house", "terrace", "farm")) \
    or (osm_tags.get("building") == "dormitory") \
    or (osm_tags.get("military") == "barracks") \
    or (osm_tags.get("landuse") == "residential") :
        return ("accomodation", "housing")
    elif (osm_tags.get("amenity") == "nursing_home") :
        return ("accomodation", "pension")
    elif (osm_tags.get("amenity") == "prison") :
        return ("accomodation", "prison")

    #Type : education
    elif (osm_tags.get("amenity") == "school") \
    or (osm_tags.get("building") == "school") :
        return ("education", "school")
    elif (osm_tags.get("amenity") in ("college", "university")) \
    or (osm_tags.get("building") in ("college", "university")) :
        return ("education", "academic")
    elif (osm_tags.get("amenity") in ("language_school", "music_school", "driving_school")) :
        return ("education", "others")

    #Type : command
    elif (osm_tags.get("amenity") == "courthouse") :
        return ("command", "law")
    elif (osm_tags.get("amenity") in ("embassy", "townhall")) \
    or (osm_tags.get("building") == "government") \
    or (osm_tags.get("office") == "diplomatic") \
    or (osm_tags.get("diplomatic")) :
        return ("command", "politics")
    elif (osm_tags.get("amenity") == "police") :
        return ("command", "police")

    #Type : office
    elif (osm_tags.get("building") in ("office", "commercial")) \
    or ("office" in osm_tags.keys() and osm_tags.get("office") not in ("diplomatic")) \
    or (osm_tags.get("amenity") == "bank") \
    or (osm_tags.get("landuse") == "commercial") :
        return ("office", "office")

    #Type :  commerce
    elif (osm_tags.get("building") == "supermarket") \
    or (osm_tags.get("shop")in ("supermarket", "convenience")) :
        return ("commerce", "supermarket")
    elif (osm_tags.get("amenity") in  ("brothel", "love_hotel", "stripclub", "swingerclub", "nightclub")) :
        return ("commerce", "nocturnal")
    elif (osm_tags.get("building") in ("kiosk", "retail") \
    or (osm_tags.get("amenity") == "marketplace") \
    or ("shop" in osm_tags.keys() and osm_tags.get("shop") not in ("mall", "department_store", "supermarket", "car_repair", "car_parts", "fuel", "convenience"))) :
        return ("commerce", "shop")
    elif (osm_tags.get("shop") in ("mall", "department_store")) :
        return ("commerce", "mall")
    elif (osm_tags.get("amenity") in ("bar", "cafe", "ice_cream", "food_court", "pub")) :
        return ("commerce","limited_restoration")
    elif (osm_tags.get("amenity") == "fast_food") :
        return ("commerce", "out_restoration")
    elif (osm_tags.get("amenity") == "restaurant") :
        if (osm_tags.get("delivery") == "yes")\
        or (osm_tags.get("takeaway") == "yes")\
        or (osm_tags.get("drive_through") == "yes") :
            return ("commerce", "out_restoration")
        else :
            return ("commerce","limited_restoration")
    elif (osm_tags.get("amenity") == "casino") \
    or (osm_tags.get("leisure") in ("adult_gaming_centre", "amusement_arcade", "escape_game")) \
    or (osm_tags.get("tourism") == "aquarium") :
        return ("commerce", "leisure_inside")
    elif (osm_tags.get("leisure") in ("summer_camp", "resort", "water_park")) \
    or (osm_tags.get("tourism") in ("attraction", "camp_site", "theme_park", "zoo")) :
        return ("commerce", "leisure_outside")
    elif (osm_tags.get("shop") in ("museum", "gallery")) \
    or (osm_tags.get("amenity") in ("arts_centre", "cinema", "theatre"))\
    or (osm_tags.get("tourism") in ("gallery", "museum")) :
        return ("commerce", "art")
    elif (osm_tags.get("leisure") in ("fitness_centre", "ice_rink", "sports_centre", "sports_hall", "swimming_pool")) \
    or (osm_tags.get("building") == "sports_hall") :
        return ("commerce", "sport_inside")
    elif (osm_tags.get("leisure") in ("golf_course", "horse_riding", "stadium")) \
    or (osm_tags.get("building") == "stadium") \
    or (osm_tags.get("landuse") == "winter_sports") :
        return ("commerce", "sport_outside")

    #Type : social
    elif (osm_tags.get("amenity") in ("kindergarten", "childcare")) :
        return ("social","kindergarten")
    elif (osm_tags.get("amenity") in ("library", "social_centre", "community_centre", "conference_centre", "events_venue")) :
        return ("social", "inside")
    elif (osm_tags.get("leisure") in ("park", "playground", "beach_resort", "fitness_station", "pitch", "track")) \
    or (osm_tags.get("landuse") == "recreation_ground") \
    or (osm_tags.get("garden:type") == "community") :
        return ("social", "park")
    elif (osm_tags.get("building") in ("cathedral", "church", "mosque", "synagogue", "temple"))\
    or (osm_tags.get("amenity") == "place_of_worship") :
        return ("social", "religious")
    elif (osm_tags.get("amenity") in ("grave_yard", "place_of_mourning", "funeral_hall")) :
        return ("social", "funeral")

    #Type : production
    elif (osm_tags.get("building") == "industrial") \
    or (osm_tags.get("landuse") in ("industrial", "port")) \
    or (osm_tags.get("power") == "plant") :
        return ("production", "industry")
    elif (osm_tags.get("building") == "construction") \
    or (osm_tags.get("landuse") == "construction") :
        return ("production", "construction")
    elif (osm_tags.get("building") in ("barn", "cowshed", "greenhouse", "stable", "sty")) :
        return ("production", "agriculture")
    elif (osm_tags.get("craft")) :
        return ("production", "craft")

    #Type : health
    elif (osm_tags.get("amenity") == "hospital") \
    or (osm_tags.get("building") == "hospital") :
        return ("health", "hospital")
    elif (osm_tags.get("amenity") == "doctors") :
        return ("health", "doctor")
    elif (osm_tags.get("amenity") in ("dentist", "veterinary", "social_facility")) \
    or (osm_tags.get("amenity") == "fire_station") \
    or (osm_tags.get("building") == "fire_station") \
    or (osm_tags.get("emergency") == "ambulance_station") :
        return ("health", "others")
    elif (osm_tags.get("amenity") == "clinic") :
        return ("health", "clinic")
    elif (osm_tags.get("amenity") == "pharmacy") :
        return ("health", "pharmacy")

    #Type : logistic
    elif (osm_tags.get("railway") in ("station", "platform")) \
    or (osm_tags.get("building") in ("train_station", "transportation")) \
    or (osm_tags.get("public_transport") in ("platform", "station")) :
        return ("logistic", "common_transport")
    elif (osm_tags.get("aeroway") == "aerodrome") \
    or (osm_tags.get("military") == "airfield") :
        return ("logistic", "airport")
    elif (osm_tags.get("amenity") == "fuel") \
    or (osm_tags.get("shop") == "fuel") :
        return ("logistic", "fuel")
    elif (osm_tags.get("shop") in ("car_repair", "car_parts")) \
    or (osm_tags.get("amenity") in ("car_rental", "vehicle_inspection")) :
        return ("logistic", "garage")
        return ("logistic", "public_transport")
    elif (osm_tags.get("amenity") == "post_office") :
        return ("logistic", "post")

    else:
        return (None, None)


class OsmHandler (osmium.SimpleHandler) :

    def __init__(self) : # network_file
        osmium.SimpleHandler.__init__(self)
        #self.__dataroad = DataRoad.DataRoad(network_file)
        self.__nodes = dict()
        self.__proj = partial(pyproj.transform, pyproj.Proj('epsg:4326'),pyproj.Proj('epsg:3857'))
        self.__dataplace = DataPlace()
        print(f"{Color.GREEN}Extracting places from osm file in progress ...{Color.RESET}")


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
        '''
        if osm_tags.get("highway") not in (None, "construction") :
            nodes = self.getNodesLocation(w.nodes)
            self.__dataroad.addRoad(id=w.id, location=self.getLocation(nodes), nodes=nodes, osm_tags=osm_tags)
        else :
        '''
        osm_tags = self.get_tags(w.tags)
        type_name, subtype_name = get_typage_place_from_osm_tags(osm_tags)
        if type_name != None and subtype_name != None :
            nodes = self.get_nodes_location(w.nodes)
            area = self.get_area(nodes)
            if (area != None) and (area >0):
                id_key = w.id
                latitude, longitude = self.get_location(nodes)
                self.__dataplace.insert_place(id_key, type_name, subtype_name, latitude, area, str(nodes), str(osm_tags))
                
        
        '''
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
        '''