from Modules.Place import DataPlace, DataRoad, setElementsFromOsm
from Modules.Tools.Style import color

def initOsmElements(osm_file, network_file) :

    setElementsFromOsm.OsmHandler(network_file=network_file).apply_file(osm_file)

def assignRoadPlace() :

    print(f"{color.GREEN}Assigning place road in progress ...{color.RESET}")

    dataplace = DataPlace.DataPlace()
    dataroad = DataRoad.DataRoad()

    for id in dataplace.getPlaces() :
        place = dataplace.getPlace(id)
        location = place.getLocation()
        road = dataroad.getNearestRoad(location)
        place.setRoad(road, change=True, check=True)
        dataroad.getRoad(road).addPlace(id)

def setPolygonTypeSumoFromOSM(path, file):

    f = open(f"{path}/{file}", "w")
    f.write("""<?xml version="1.0" encoding="UTF-8"?>
<polygonTypes>
    <polygonType id="building" name="building" color="0.0,0.0,1.0" layer="1"/>
</polygonTypes>
    """)
    f.close()

    return file

def getTypePlaceFromOSM(osm_tags) :

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

def initTypageDataPlace() :

    dataplace=DataPlace.DataPlace()

    dataplace.addTypePlace("accomodation")
    type = dataplace.getType("accomodation")
    type.addSubtypePlace("hotel")
    type.addSubtypePlace("hotel")
    type.addSubtypePlace("housing")
    type.addSubtypePlace("pension")
    type.addSubtypePlace("prison")

    dataplace.addTypePlace("education")
    type = dataplace.getType("education")
    type.addSubtypePlace("school")
    type.addSubtypePlace("academic")
    type.addSubtypePlace("others")

    dataplace.addTypePlace("command")
    type = dataplace.getType("command")
    type.addSubtypePlace("law")
    type.addSubtypePlace("politics")
    type.addSubtypePlace("police")

    dataplace.addTypePlace("office")
    type = dataplace.getType("office")
    type.addSubtypePlace("office")

    dataplace.addTypePlace("commerce")
    type = dataplace.getType("commerce")
    type.addSubtypePlace("supermarket")
    type.addSubtypePlace("nocturnal")
    type.addSubtypePlace("shop")
    type.addSubtypePlace("mall")
    type.addSubtypePlace("limited_restoration")
    type.addSubtypePlace("out_restoration")
    type.addSubtypePlace("leisure_inside")
    type.addSubtypePlace("leisure_outside")
    type.addSubtypePlace("art")
    type.addSubtypePlace("sport_inside")
    type.addSubtypePlace("sport_outside")

    dataplace.addTypePlace("social")
    type = dataplace.getType("social")
    type.addSubtypePlace("kindergarten")
    type.addSubtypePlace("inside")
    type.addSubtypePlace("park")
    type.addSubtypePlace("religious")
    type.addSubtypePlace("funeral")

    dataplace.addTypePlace("production")
    type = dataplace.getType("production")
    type.addSubtypePlace("industry")
    type.addSubtypePlace("construction")
    type.addSubtypePlace("agriculture")
    type.addSubtypePlace("craft")

    dataplace.addTypePlace("health")
    type = dataplace.getType("health")
    type.addSubtypePlace("hospital")
    type.addSubtypePlace("doctor")
    type.addSubtypePlace("others")
    type.addSubtypePlace("clinic")
    type.addSubtypePlace("pharmacy")

    dataplace.addTypePlace("logistic")
    type = dataplace.getType("logistic")
    type.addSubtypePlace("common_transport")
    type.addSubtypePlace("airport")
    type.addSubtypePlace("fuel")
    type.addSubtypePlace("garage")
    type.addSubtypePlace("post")

    return dataplace
