from modules.tools.singleton import Singleton
from modules.tools.style import Color
import os
import sqlite3


class Place():
    
    def __init__(self, place):
        self.place = place 
    
    def __getitem__(self, key) :
        values = {
            'id' : self.place[0],
            'type' : self.place[1],
            'subtype' : self.place[2],
            'typage' : [self.place[1], self.place[2]],
            'latitude' : self.place[3],
            'longitude' : self.place[4],
            'location' : [self.place[3], self.place[4]],
            'area' : self.place[5],
            'road_id' : self.place[6],
            'nodes' : eval(self.place[7]),
            'tags' : eval(self.place[8])
            }
        if key in values.keys():
            return values[key]
        elif key in ['all', 'values']:
            return values
        else:
            raise KeyError(f"Key '{key}' not found.")


class DataPlaces(metaclass=Singleton):
    
    def __init__(self, database_path, raise_error_on_duplicate_id=False) :
        os.makedirs(os.path.dirname(database_path), exist_ok=True)
        self.database_path = database_path
        self.raise_error_on_duplicate_id = raise_error_on_duplicate_id
        
    def __start_connection_db(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        
    def __end_connection_db(self):
        self.cursor.close()
        self.connection.close()
    
    def create_database(self) :
        self.__start_connection_db()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Places (
            id INTEGER PRIMARY KEY, 
            type TEXT,
            subtype TEXT,
            latitude REAL,
            longitude REAL,
            area REAL,
            road_id INTEGER,
            nodes TEXT,
            tags TEXT
            )''')
        self.__end_connection_db()
        
    def insert_place(self, id_key, type_name, subtype_name, latitude, longitude, 
                     area, road_id=None, nodes="None", tags="None"):
        self.__start_connection_db()
        # Check if the id_key already exists
        self.cursor.execute("SELECT id FROM Places WHERE id = ?", 
                            (id_key,))
        existing_id = self.cursor.fetchone()
        if existing_id:
            if self.raise_error_on_duplicate_id:
                raise ValueError(f"ID {id_key} already exists in the places "
                                 "database.\n")
            else:
                print(f"{Color.RED}Warning:{Color.RESET} ID {id_key} already "
                      "exists in the places database.\n")
        else:
            # Insert the place
            self.cursor.execute('''INSERT INTO Places (
                id, type, subtype, latitude, longitude, area, road_id, nodes, tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (id_key, type_name, subtype_name, latitude, longitude, area, road_id, nodes, tags))
            self.connection.commit()
        self.__end_connection_db()
            
    def assign_road_id_to_place(self, place_id, road_id):
        self.__start_connection_db()
        # Check if both id exists
        self.cursor.execute('''UPDATE Places SET road_id = ? WHERE id = ?''',
                            (road_id, place_id))
        self.connection.commit()
        self.__end_connection_db()

    def remove_place(self, id_key):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM Places WHERE id = ?", 
                            (id_key,))
        self.connection.commit()
        self.__end_connection_db()
        
    def reset_database(self):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM Places")
        self.connection.commit()
        self.__end_connection_db()

    """Get places"""
    
    def get_all_places(self) :
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Places")
        all_places = self.cursor.fetchall()
        self.__end_connection_db()
        return all_places
    
    def get_typage_places(self, type_name, subtype_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Places WHERE type = ? AND subtype = ?", 
                            (type_name, subtype_name))
        typage_places = self.cursor.fetchall()
        self.__end_connection_db()
        return typage_places
    
    def get_type_places(self, type_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Places WHERE type = ? ", 
                            (type_name,))
        type_places = self.cursor.fetchall()
        self.__end_connection_db()
        return type_places
    
    def get_id_place(self, id_key):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Places WHERE id = ? ", 
                            (id_key,))
        id_place = self.cursor.fetchall()
        self.__end_connection_db()
        return id_place
    
    """List ids"""
    
    def list_all_ids(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT id FROM Places")
        all_ids = [row[0] for row in self.cursor.fetchall()]
        self.__end_connection_db()
        return all_ids
    
    def list_ids_by_typage(self, type_name, subtype_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT id FROM Places WHERE type = ? AND subtype = ?", 
                            (type_name, subtype_name))
        typage_ids = self.cursor.fetchall()
        self.__end_connection_db()
        return typage_ids
    
    def list_ids_by_type(self, type_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT id FROM Places WHERE type = ?", 
                            (type_name,))
        type_ids = self.cursor.fetchall()
        self.__end_connection_db()
        return type_ids
    
    """List unique typage"""
    
    def list_unique_typage(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT DISTINCT type, subtype FROM Places")
        unique_typages = self.cursor.fetchall()
        self.__end_connection_db()
        return unique_typages

    def list_unique_subtypes_for_type(self, type_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT DISTINCT subtype FROM Places WHERE type = ?", 
                            (type_name,))
        unique_subtypes = [row[0] for row in self.cursor.fetchall()]
        self.__end_connection_db()
        return unique_subtypes

    """Count places"""

    def count_places(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM Places")
        count_all = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_all
    
    def count_places_by_typage(self, type_name, subtype_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM Places WHERE type = ? AND subtype = ?", 
                            (type_name, subtype_name))
        count_typage = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_typage
    
    def count_places_by_type(self, type_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM Places WHERE type = ?", 
                            (type_name,))
        count_type = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_type
    
    """Total area"""
    
    def total_typage_area(self, type_name, subtype_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT SUM(area) FROM Places WHERE type = ? AND subtype = ?", 
                            (type_name, subtype_name))
        total_typage_area = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return total_typage_area 
    
    def total_type_area(self, type_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT SUM(area) FROM Places WHERE type = ?", 
                            (type_name,))
        total_type_area = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return total_type_area 
        
    

'''----------------------------------------------------------------> DEPRECATED

from modules.tools.singleton import Singleton
from modules.tools import distance
from modules.tools.style import Color
from random import sample


class DataPlace (metaclass=Singleton) :

    __next_id_place = 1

    def __init__(self) :
        self.__type = dict()
        self.__place = dict()

    def __increment_place(self) :
        self.__next_id_place += 1

    def __get_id_place(self) :
        return self.__next_id_place

    def __get_typology(self) :
        typology = list()
        for type in self.get_types() :
            for subtype in self.get_type(type).get_subtypes() :
                typology.append([type, subtype])
        return typology

    def __validTypage(self, typage):
        full_typage = self.__getFullTypage()
        valid_typage = list()
        if type(typage) in (tuple, list) :
            for elem in typage :
                if type(elem) in (tuple, list) and len(elem) == 2 :
                    if elem in full_typage :
                        valid_typage.append(list(elem))
                    else :
                        print(f"{color.RED}Error :{color.RESET} {elem} is not in typage of DataPlace")
                else :
                    print(f"{color.RED}Error :{color.RESET} Typage list must contain lists as [type, subtype]")
        else :
            print(f"{color.RED}Error :{color.RESET} Typage must be a list")
        return valid_typage

    def getTypes(self) :
        l = list()
        for key in self.__type.keys() :
            l.append(key)
        return l

    def getType(self, name) :
        if name in self.getTypes() :
            return self.__type[name]
        else :
            print(f"{color.RED}Error :{color.RESET} Type {color.CYAN}{name}{color.RESET} is not in DataPlace")
            return None

    def getPlaces(self) :
        l = list()
        for key in self.__place.keys() :
            l.append(key)
        return l

    def getPlace(self, id) :
        if id in self.getPlaces() :
            return self.__place[id]
        else :
            print(f"{color.RED}Error :{color.RESET} Place {color.BLUE}{id}{color.RESET} is not in DataPlace")
            return None

    def addPlace(self, location, type, subtype, id=None, autoId=True, **kwargs) :
        if id in self.getPlaces() :
            print(f"{color.RED}Error :{color.RESET} Place {color.BLUE}{id}{color.RESET} is already in DataPlace")
        elif autoId == True :
            id = self.__getIdPlace()
            while id in self.getPlaces() :
                self.__incrementPlace()
                id = self.__getIdPlace()
            print(f"AutoId found unused id {color.BLUE}{id}{color.RESET} in DataPlace")
        if id not in self.getPlaces() :
            if type in self.getTypes() :
                if subtype in self.getType(type).getSubtypes() :
                    self.__place[id] = self.Place (id, location, type, subtype, **kwargs)
                    print(f"Place {color.BLUE}{id}{color.RESET} has been added to DataPlace")
                    self.getType(type).getSubtype(subtype).addLinkPlace(id)
                else :
                    print(f"{color.RED}Error :{color.RESET} Subtype {color.CYAN}{subtype}{color.RESET} is not in type {type}")
            else :
                print(f"{color.RED}Error :{color.RESET} Type {color.CYAN}{type}{color.RESET} is not in DataPlace")

    def removePlace(self, id) :
        place = self.getPlace(id) #Print Error
        if place != None :
            type, subtype = place.getTypage()
            del self.__place[id]
            print(f"Place {color.BLUE}{id}{color.RESET} has been removed from DataPlace")
            self.getType(type).getSubtype(subtype).removeLinkPlace(id)
            #Remove others links ...

    def addTypePlace(self, name) :
        if name in self.getTypes() :
            print(f"{color.RED}Error :{color.RESET} Type {color.BLUE}{type}{color.RESET} is already in DataPlace")
        else :
            self.__type[name] = self.TypePlace(name)
            print(f"Type {color.CYAN}{name}{color.RESET} has been added to DataPlace")

    def removeTypePlace(self, name=None, select=False) :
        type = getType(name) #Print Error
        if type == None :
            if select == True :
                for type in self.getTypes() :
                    print(type)
                name = input(f"{color.GREEN}Select type name to remove :{color.RESET}")
                type = getType(name) #Print Error
        if type != None :
            full = False
            subtypes = type.getSubtypes()
            subtype = 0
            while full == False and subtype < len(subtypes) :
                if len(type.getSubtype(subtypes[subtype]).getPlaces()) > 0 :
                    full = True
                subtype += 1
            if full == False :
                del self.__type[name]
                print(f"Type {color.CYAN}{type.getName()}{color.RESET} has been removed from DataPlace")
            else :
                print(f"{color.RED}Error :{color.RESET} Type {color.CYAN}{type.getName()}{color.RESET} still contains places")

    def filterPlace(self, location, typage=None, order=None, distance_max=None, distance_min=0, area_max=None, area_min=0) :
        typage = self.__validTypage(typage)
        if typage == None :
            print(f"{color.RED}Warning :{color.RESET} Typage not recognized")
            typage = self.__getFullTypage()
        filter = dict()
        for elem in typage :
            for type, subtype in typage :
                subtype_filter = self.getType(type).getSubtype(subtype).filterPlace(location=location, order=None, distance_max=distance_max, distance_min=distance_min, area_max=area_max, area_min=area_min)["filter"]
                fitler.extend(subtype_filter)
        if order == True :
            order = list()
            for elem in sorted((filter[place][1], place) for place in filter.keys()) :
                order.append([elem[0], elem[1]])
        return {"location":location, "filter":filter, "order":order}

    def countPlace(self, show=True) :
        l = list()
        sum = 0
        if len(self.getTypes()) > 0 :
            for type in self.getTypes() :
                count = self.getType(type).countPlace(show=False)
                l.extend(count)
                sum += count[-1][-1]
        l.insert(0, ["DataPlace", "Total", sum])
        if show == True :
            print(f"Total {color.CYAN}{l[0][0].upper()}{color.RESET} : {l[0][2]} places\n_________________________")
            for elem in l[1:] :
                if elem[1] == "Total" :
                    print(f"Total {color.CYAN}{elem[0].upper()}{color.RESET} : {elem[2]} places")
                else :
                    print(f"  {color.CYAN}{elem[1]}{color.RESET} : {elem[2]} places")
        return l

    def countArea(self, show=True) :
        l = list()
        sum = 0
        if len(self.getTypes()) > 0 :
            for type in self.getTypes() :
                count = self.getType(type).countArea(show=False)
                l.extend(count)
                sum += count[-1][-1]
        l.insert(0, ["DataPlace", "Total", sum])
        if show == True :
            print(f"Total {color.CYAN}{l[0][0].upper()}{color.RESET} : {l[0][2]}\n_________________________")
            for elem in l[1:] :
                if elem[1] == "Total" :
                    print(f"Total {color.CYAN}{elem[0].upper()}{color.RESET} : {elem[2]}")
                else :
                    print(f"  {color.CYAN}{elem[1]}{color.RESET} : {elem[2]}")
        return l

    def __str__(self) :
        kwargs = dict()
        kwargs["indent"] = 1
        kwargs["typage"] = kwargs.get("typage", True)
        kwargs["type"] = kwargs.get("type", True)
        kwargs["place"] = kwargs.get("place", False)
        kwargs["limit"] = kwargs.get("limit", 5)

        string = f"{color.UNDERLINE}DataPlace :{color.RESET}"
        for type in self.getTypes() :
            string += f"\n\n{self.getType(type).__str__(**kwargs)}"
        return string

    def __repr__(self) :
        return self.__str__()

    class TypePlace() :

        def __init__(self, name) :
            self.__subtype = dict()
            self.__name = str(name)

        def getName(self) :
            return self.__name

        def getSubtypes(self) :
            l = list()
            for key in self.__subtype.keys():
                l.append(key)
            return l

        def getSubtype(self, name) :
            if name in self.getSubtypes() :
                return self.__subtype[name]
            else :
                print(f"{color.RED}Error :{color.RESET} Subtype {color.CYAN}{name}{color.RESET} is not in type {self.getName()}")
                return None

        def getPlaces(self) :
            l = list()
            for subtype in self.getSubtypes() :
                l.extend(self.getSubtype(subtype).getPlaces())
            return l

        def addSubtypePlace(self, name) :
            if name in self.getSubtypes() :
                print(f"{color.RED}Error :{color.RESET} Subtype {color.CYAN}{name}{color.RESET} is already in type {self.getName()}")
            else :
                self.__subtype[name] = self.SubtypePlace(name, self.getName())
                print(f"Subtype {color.CYAN}{name}{color.RESET} has been added to type {self.getName()}")

        def removeSubtypePlace(self, name=None, select=False) :
            subtype = getSubtype(name) #Print Error
            if subtype == None :
                if select == True :
                    for subtype in self.getSubtypes() :
                        print(subtype)
                    name = input(f"{color.GREEN}Select subtype name to remove :{color.RESET}")
                    subtype = getSubtype(name) #Print Error
            if subtype != None :
                if len(subtype.getPlaces()) == 0 :
                    del self.__subtype[name]
                    print(f"Subtype {color.CYAN}{subtype.getName()}{color.RESET} has been removed from type {self.getName()}")
                else :
                    print(f"{color.RED}Error :{color.RESET} Type {color.CYAN}{subtype.getName()}{color.RESET} still contains places")

        def filterPlace(self, location, order=None, distance_max=None, distance_min=0, area_max=None, area_min=0) :
            filter = dict()
            for subtype in self.getSubtypes() :
                for id in self.getSubtype(subtype).getPlaces() :
                    place = DataPlace().getPlace(id)
                    distance = Distance.getMathDistance(place.getLocation(), location)
                    area = place.getArea()
                    if (distance_max == None) or (distance_max != None and distance_max >= distance) :
                        if (area_max == None) or (area_max != None and area_max >= area) :
                            if (area_min <= area) and (distance_min <= distance) :
                                filter[id] = [place, distance]
            if order == True :
                order = list()
                for elem in sorted((filter[place][1], place) for place in filter.keys()) :
                    order.append([elem[0], elem[1]])
            return {"location":location, "filter":filter, "order":order}

        def countPlace(self, show=True) :
            l = list()
            sum = 0
            if len(self.getSubtypes()) > 0 :
                for subtype in self.getSubtypes() :
                    count = self.getSubtype(subtype).countPlace(show=False)
                    l.extend(count)
                    sum += count[-1][-1]
            l.append([self.getName(), "Total", sum])
            if show == True :
                for elem in l :
                    if elem[1] == "Total" :
                        print(f"Total {color.CYAN}{elem[0].upper()}{color.RESET} : {elem[2]} places")
                    else :
                        print(f"  {color.CYAN}{elem[1]}{color.RESET} : {elem[2]} places")
            return l

        def countArea(self, show=True) :
            l = list()
            sum = 0
            if len(self.getSubtypes()) > 0 :
                for subtype in self.getSubtypes() :
                    count = self.getSubtype(subtype).countArea(show=False)
                    l.extend(count)
                    sum += count[-1][-1]
            l.append([self.getName(), "Total", sum])
            if show == True :
                for elem in l :
                    if elem[1] == "Total" :
                        print(f"Total {color.CYAN}{elem[0].upper()}{color.RESET} : {elem[2]}")
                    else :
                        print(f"  {color.CYAN}{elem[1]}{color.RESET} : {elem[2]}")
            return l

        def __str__(self, **kwargs) :
            indent = kwargs.get("indent", 0)
            kwargs["indent"] = indent+1
            kwargs["typage"] = kwargs.get("typage", True)
            kwargs["type"] = kwargs.get("type", False)
            kwargs["place"] = kwargs.get("place", False)
            kwargs["limit"] = kwargs.get("limit", 10)

            string = "\t"*indent + f"{color.UNDERLINE}Type :{color.RESET} {color.CYAN}{self.getName()}{color.RESET}"
            for subtype in self.getSubtypes() :
                string += f"\n\n{self.getSubtype(subtype).__str__(**kwargs)}"
            return string

        def __repr__(self) :
            return self.__str__()

        class SubtypePlace () :
            def __init__(self, name, type) :
                self.__feature = dict()
                self.__place = list()
                self.__name = str(name)
                self.__type = str(type)

            def getName(self) :
                return self.__name

            def getFeatures(self) :
                l = list()
                for key in self.__feature.keys() :
                    l.append(key)
                return l

            def getFeature(self, feature) :
                if feature in self.getFeatures() :
                    return self.__feature[feature]
                else :
                    print(f"{color.RED}Error :{color.RESET} Feature {color.CYAN}{feature}{color.RESET} is not in features")
                    return None

            def getPlaces(self) :
                return self.__place

            def getType(self) :
                return self.__type

            def addFeature(self, feature, value, change=False) :
                if feature in self.getFeatures() :
                    print(f"{color.RED}Error :{color.RESET} Feature {color.CYAN}{feature}{color.RESET} is already in subtype {self.getName()} with value : {self.getFeature(feature)}")
                    if change == True :
                        self.__feature[feature] = value
                        print(f"Value of feature {color.CYAN}{feature}{color.RESET} has been changed to sutbype {self.getName()}")
                else :
                    self.__feature[feature] = value
                    print(f"Feature {color.CYAN}{feature}{color.RESET} has been added to sutbype {self.getName()}")

            def removeFeature(self, feature=None, select=False) :
                feature = getFeature(feature) #Print Error
                if feature == None :
                    if select == True :
                        for feature in self.getFeatures() :
                            print(f"Feature {feature} with value {self.getFeature(feature)}")
                        name = input(f"{color.GREEN}Select subtype feature to remove :{color.RESET}")
                        feature = getFeature(name) #Print Error
                if feature != None :
                    if len(subtype.getPlaces()) == 0 :
                        del self.__subtype[name]
                        print(f"Feature {color.CYAN}{feature}{color.RESET} has been removed from subtype {self.getName()}")

            def addPlace(self, location, id=None, autoId=None, **kwargs):
                DataPlace().addPlace(id=id, autoId=autoId, location=location, type=self.getType(), subtype=self.getName(), **kwargs)

            def addLinkPlace(self, id) :
                place = DataPlace().getPlace(id) # Print Error
                if place != None :
                    type, subtype = place.getTypage()
                    if type == self.getType() and subtype == self.getName() :
                        if id in self.getPlaces() :
                            print(f"{color.RED}Error :{color.RESET} Place {color.BLUE}{id}{color.RESET} is already in typage : {self.getType()} | {self.getName()}")
                        else :
                            self.__place.append(id)
                            print(f"Place {color.BLUE}{id}{color.RESET} has been added to typage : {self.getType()} | {self.getName()}")
                    else :
                        print(f"{color.RED}Error :{color.RESET} Place {color.BLUE}{id}{color.RESET} is link to an other typage : {type} | {subtype}")

            def removeLinkPlace(self, id) :
                if id in DataPlace().getPlaces() :
                    print(f"{color.RED}Error :{color.RESET} Place {color.BLUE}{id}{color.RESET} is still in DataPlace")
                else :
                    if id in self.getPlaces() :
                        self.__place.remove(id)
                        print(f"Place {color.BLUE}{id}{color.RESET} has been removed from typage : {self.getType()} | {self.getName()}")
                    else :
                        print(f"{color.RED}Error :{color.RESET} Place {color.BLUE}{id}{color.RESET} is no longer linked to typage : {self.getType()} | {self.getName()}")

            def filterPlace(self, location, order=None, distance_max=None, distance_min=0, area_max=None, area_min=0) :
                filter = dict()
                for id in self.getPlaces() :
                    place = DataPlace().getPlace(id)
                    distance = Distance.getMathDistance(place.getLocation(), location)
                    area = place.getArea()
                    if (distance_max == None) or (distance_max != None and distance_max >= distance) :
                        if (area_max == None) or (area_max != None and area_max >= area) :
                            if (area_min <= area) and (distance_min <= distance) :
                                filter[id] = [place, distance]
                if order == True :
                    order = list()
                    for elem in sorted((filter[place][1], place) for place in filter.keys()) :
                        order.append([elem[0], elem[1]])
                return {"location":location, "filter":filter, "order":order}

            def countPlace(self, show=True) :
                l = list()
                l.append([self.getType(), self.getName(), len(self.getPlaces())])
                if show == True :
                    print(f"  {color.CYAN}{l[0][1]}{color.RESET} : {l[0][2]} places")
                return l

            def countArea(self, show=True) :
                dataplace = DataPlace()
                l = list()
                sum = 0
                for place in self.getPlaces() :
                    sum += dataplace.getPlace(place).getArea()
                l.append([self.getType(), self.getName(), sum])
                if show == True :
                    print(f"  {color.CYAN}{l[0][1]}{color.RESET} : {l[0][2]} places")
                return l

            def __str__(self, **kwargs) :
                indent = kwargs.get("indent", 0)
                kwargs["indent"] = indent + 1
                type = kwargs.get("type", True)
                place = kwargs.get("place", True)
                limit = kwargs.get("limit", 10)
                kwargs["typage"] = kwargs.get("typage", False)

                string = "\t"*indent + f"{color.UNDERLINE}Subtype :{color.RESET} {color.CYAN}{self.__name}{color.RESET}"
                if type == True :
                    string += f", from {color.CYAN}{self.__type}{color.RESET}"
                features = self.getFeatures()
                if len(features) > 0 :
                    string += "\n\t" + "\t"*indent + "Features :"
                    for feature in features :
                        if type(self.getFeature(feature)) == dict :
                            dic = self.getFeature(feature)
                            for key, value in dic.items():
                                string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{feature}{color.RESET} | {key} : {value}"
                        else :
                            string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{feature}{color.RESET} : {self.getFeature(feature)}"
                places = self.getPlaces()
                if len(places) > 0 :
                    if len(places) < limit or limit == None :
                        size = len(places)
                    else :
                        size = limit
                    r = sample(places, size)
                    if place == False :
                        string += "\n\t" + "\t"*indent + "Places :"
                        for id in r :
                            string += "\n\t\t" + "\t"*indent + f"{color.BLUE}{id}{color.RESET}"
                    else :
                        for id in r :
                            string += f"\n\n{DataPlace().getPlace(id).__str__(**kwargs)}"
                    if len(places) > limit :
                        string += "\n\t\t" + "\t"*indent + f"{color.BLUE}...{color.RESET}"

                return string

            def __repr__(self) :
                return self.__str__()

    class Place() :
        def __init__(self, id, location, type, subtype,**kwargs) :
            self.__typage = [str(type), str(subtype)]
            self.__id = id
            self.__location= location
            self.__area = kwargs.get("area", 0)
            self.__nodes = kwargs.get("nodes", None)
            self.__road = None
            self.__feature = dict()
            if kwargs.get("osm_tags") :
                self.__feature["osm_tags"] = kwargs.get("osm_tags")


        def getId(self) :
            return self.__id

        def getLocation(self) :
            return self.__location

        def getArea(self) :
            return self.__area

        def getRoad(self) :
            return self.__road

        def getTypage(self) :
            return self.__typage

        def getType(self) :
            return self.__typage[0]

        def getSubtype(self):
            return self.__typage[1]

        def getNodes (self) :
            return self.__nodes

        def getFeatures(self) :
            l = list()
            for key in self.__feature.keys() :
                l.append(key)
            return l

        def getFeature(self, feature) :
            if feature in self.getFeatures() :
                return self.__feature[feature]
            else :
                print(f"{color.RED}Error :{color.RESET} Feature {color.CYAN}{feature}{color.RESET} is not in features")
                return None

        def setRoad(self, road, change=None, check=None) :
            if check == None :
                road = DataRoad.DataRoad().getRoad(road) #Print Error
                if road != None :
                    check = True
            if check == True :
                current = self.getRoad()
                if current != None :
                    print(f"{color.RED}Warning :{color.RESET} Road {color.CYAN}{current}{color.RESET} has already been linked to place : {self.getId()}")
                    if change == True :
                        self.__road = road
                        print(f"Road {color.CYAN}{road}{color.RESET} has replaced {current} to place {self.getId()}")
                else :
                    self.__road = road
                    print(f"Road {color.CYAN}{road}{color.RESET} has been linked to place {self.getId()}")

        def addFeature(self, feature, value, change=False) :
            if feature in self.getFeatures() :
                print(f"{color.RED}Error :{color.RESET} Feature {color.CYAN}{feature}{color.RESET} is already in place {self.getId()} with value : {self.getFeature(feature)}")
                if change == True :
                    self.__feature[feature] = value
                    print(f"Value of feature {color.CYAN}{feature}{color.RESET} has been changed to place {self.getId()}")
            else :
                self.__feature[feature] = value
                print(f"Feature {color.CYAN}{feature}{color.RESET} has been added to place {self.getId()}")

        def removeFeature(self, feature=None, select=False) :
            feature = getFeature(feature) #Print Error
            if feature == None :
                if select == True :
                    for feature in self.getFeatures() :
                        print(f"Feature {feature} with value {self.getFeature(feature)}")
                    name = input(f"{color.GREEN}Select place feature to remove :{color.RESET}")
                    feature = getFeature(name) #Print Error
            if feature != None :
                if len(subtype.getPlaces()) == 0 :
                    del self.__subtype[name]
                    print(f"Feature {color.CYAN}{feature}{color.RESET} has been removed from place {self.getId()}")

        def __str__(self, **kwargs) :
            indent = kwargs.get("indent", 0)
            typage = kwargs.get("typage", True)

            string = "\t"*indent + f"{color.UNDERLINE}Place :{color.BLUE}{self.getId()}{color.RESET}"
            if typage == True :
                string += "\n\t" + "\t"*indent + f"type : {color.CYAN}{self.getType()}{color.RESET}"
                string += "\n\t" + "\t"*indent + f"subtype : {color.CYAN}{self.getSubtype()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"location : {color.CYAN}{self.getLocation()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"area : {color.CYAN}{self.getArea()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"road : {color.CYAN}{self.getRoad()}{color.RESET}"
            features=self.getFeatures()
            if len(features)>0:
                string += "\n\t" + "\t"*indent + "Features :"
                for feature in features :
                    if type(self.getFeature(feature)) == dict :
                        dic = self.getFeature(feature)
                        for key, value in dic.items():
                            string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{feature}{color.RESET} | {key} : {value}"
                    else :
                        string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{feature}{color.RESET} : {self.getFeature(feature)}"
            return string

        def __repr__(self) :
            return self.__str__(typage=True)

'''