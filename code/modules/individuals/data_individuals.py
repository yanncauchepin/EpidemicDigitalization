from modules.tools.singleton import Singleton
from modules.tools.style import Color
import os
import sqlite3


class Individual():
    
    def __init__(self, individual):
        self.individual = individual
    
    def __getitem__(self, key) :
        values = {
            'id' : self.individual[0],
            'type' : self.individual[1],
            'subtype' : self.individual[2],
            'typage' : [self.individual[1], self.individual[2]],
            'age' : self.individual[3],
            'home_place_id' : self.individual[4],
            'home_individuals_id' : eval(self.individual[5]),
            'work_place_id' : self.individual[6],
            'work_individuals_id' : eval(self.individual[7]),
            'transport' : eval(self.individual[8]),
            'featues' : eval(self.individual[9])
            }
        if key in values.keys():
            return values[key]
        elif key in ['all', 'values']:
            return values
        else:
            raise KeyError(f"Key '{key}' not found.")


class DataIndividuals(metaclass=Singleton):
    
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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Individuals (
            id INTEGER PRIMARY KEY, 
            type TEXT,
            subtype TEXT,
            age INTEGER,
            home_place_id INTEGER,
            home_individuals_id TEXT,
            work_place_id INTEGER,
            work_individuals_id TEXT,
            transport TEXT,
            tags TEXT
            )''')
        self.__end_connection_db()
        
    def insert_individual(self, type_name, subtype_name, age, home_place_id=None, 
                     home_individuals_id="None", work_place_id=None, 
                     work_individuals_id="None", transport="None",
                     tags="None"):
        self.__start_connection_db()
        self.cursor.execute('''INSERT INTO Individuals (
            type, subtype, age, home_place_id, home_individuals_id, 
            work_place_id, work_individuals_id, transport, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (type_name, subtype_name, age, home_place_id, home_individuals_id, 
         work_place_id, work_individuals_id, transport, tags))
        self.connection.commit()
        self.__end_connection_db()
            
    def assign_home_place_id_to_individual(self, individual_id, home_place_id):
        self.__start_connection_db()
        # Check if both id exists
        self.cursor.execute('''UPDATE Individuals SET home_place_id = ? WHERE id = ?''',
                            (individual_id, home_place_id))
        self.connection.commit()
        self.__end_connection_db()
    
    def assign_home_individuals_id_to_individual(self, individual_id, home_individuals_id):
        self.__start_connection_db()
        # Check if both id exists
        self.cursor.execute('''UPDATE Individuals SET home_individuals_id = ? WHERE id = ?''',
                            (individual_id, home_individuals_id))
        self.connection.commit()
        self.__end_connection_db()

    def assign_work_place_id_to_individual(self, individual_id, work_place_id):
        self.__start_connection_db()
        # Check if both id exists
        self.cursor.execute('''UPDATE Individuals SET work_place_id = ? WHERE id = ?''',
                            (individual_id, work_place_id))
        self.connection.commit()
        self.__end_connection_db()
    
    def assign_work_individuals_id_to_individual(self, individual_id, work_individuals_id):
        self.__start_connection_db()
        # Check if both id exists
        self.cursor.execute('''UPDATE Individuals SET work_individuals_id = ? WHERE id = ?''',
                            (individual_id, work_individuals_id))
        self.connection.commit()
        self.__end_connection_db()
        
    def assign_transport_to_individual(self, individual_id, transport):
        self.__start_connection_db()
        # Check if both id exists
        self.cursor.execute('''UPDATE Individuals SET transport = ? WHERE id = ?''',
                            (individual_id, transport))
        self.connection.commit()
        self.__end_connection_db()

    def remove_place(self, id_key):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM Individuals WHERE id = ?", 
                            (id_key,))
        self.connection.commit()
        self.__end_connection_db()
        
    def reset_database(self):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM Individuals")
        self.connection.commit()
        self.__end_connection_db()

    """Get places"""
    
    def get_all_individuals(self) :
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Individuals")
        all_individuals = self.cursor.fetchall()
        self.__end_connection_db()
        return all_individuals
    
    def get_typage_individuals(self, type_name, subtype_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Individuals WHERE type = ? AND subtype = ?", 
                            (type_name, subtype_name))
        typage_individuals = self.cursor.fetchall()
        self.__end_connection_db()
        return typage_individuals
    
    def get_type_individuals(self, type_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Individuals WHERE type = ? ", 
                            (type_name,))
        type_individuals = self.cursor.fetchall()
        self.__end_connection_db()
        return type_individuals
    
    def get_id_individual(self, id_key):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Individuals WHERE id = ? ", 
                            (id_key,))
        id_individual = self.cursor.fetchall()
        self.__end_connection_db()
        return id_individual
    
    """List ids"""
    
    def list_all_ids(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT id FROM Individuals")
        all_ids = [row[0] for row in self.cursor.fetchall()]
        self.__end_connection_db()
        return all_ids
    
    def list_ids_by_typage(self, type_name, subtype_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT id FROM Individuals WHERE type = ? AND subtype = ?", 
                            (type_name, subtype_name))
        typage_ids = self.cursor.fetchall()
        self.__end_connection_db()
        return typage_ids
    
    def list_ids_by_type(self, type_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT id FROM Individuals WHERE type = ?", 
                            (type_name,))
        type_ids = self.cursor.fetchall()
        self.__end_connection_db()
        return type_ids
    
    """List unique typage"""
    
    def list_unique_typage(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT DISTINCT type, subtype FROM Individuals")
        unique_typages = self.cursor.fetchall()
        self.__end_connection_db()
        return unique_typages

    def list_unique_subtypes_for_type(self, type_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT DISTINCT subtype FROM Individuals WHERE type = ?", 
                            (type_name,))
        unique_subtypes = [row[0] for row in self.cursor.fetchall()]
        self.__end_connection_db()
        return unique_subtypes

    """Count individuals"""

    def count_individuals(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM Individuals")
        count_all = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_all
    
    def count_individuals_by_typage(self, type_name, subtype_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM Individuals WHERE type = ? AND subtype = ?", 
                            (type_name, subtype_name))
        count_typage = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_typage
    
    def count_individuals_by_type(self, type_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM Individuals WHERE type = ?", 
                            (type_name,))
        count_type = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_type
    

'''----------------------------------------------------------------> DEPRECATED

from Modules.Script import DataScript
from Modules.Infection import DataInfection
from Modules.Tools import Singleton
from Modules.Tools.Style import color
from random import sample

class DataPerson (metaclass=Singleton.Singleton) :

    __nextIdPerson = 1

    def __init__(self) :
        self.__type=dict()
        self.__person=dict()

    def __incrementPerson(self):
        self.__nextIdPerson += 1

    def __getIdPerson(self) :
        return self.__nextIdPerson

    def __getFullTypage(self) :
        typage = list()
        for type in self.getTypes() :
            for subtype in self.getType(type).getSubtypes() :
                typage.append([type, subtype])
        return typage

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
            print(f"\n{color.RED}Error :{color.RESET} Type {color.CYAN}{name}{color.RESET} is not in DataPerson")
            return None

    def getPeople(self) :
        l = list()
        for key in self.__person.keys() :
            l.append(key)
        return l

    def getPerson(self, id) :
        if id in self.getPeople():
            return self.__person[id]
        else :
            print(f"\n{color.RED}Error :{color.RESET} Person {color.BLUE}{id}{color.RESET} is not in DataPerson")
            return None

    def addPerson(self, age, type, subtype, id=None, autoId=False, **kwargs) :
        if id in self.getPeople() :
            print(f"{color.RED}Error :{color.RESET} Person {color.BLUE}{id}{color.RESET} is already in DataPerson")
        elif autoId == True :
            id = self.__getIdPerson()
            while id in self.getPeople() :
                self.__incrementPerson()
                id = self.__getIdPerson()
            print(f"AutoId found unused id {color.BLUE}{id}{color.RESET} in DataPerson")
        if id not in self.getPeople() :
            if type in self.getTypes() :
                if subtype in self.getType(type).getSubtypes() :
                    self.__person[id] = self.Person (id, age, type, subtype, **kwargs)
                    print(f"Person {color.BLUE}{id}{color.RESET} has been added to DataPerson")
                    self.getType(type).getSubtype(subtype).addLinkPerson(id)
                else :
                    print(f"{color.RED}Error :{color.RESET} Subtype {color.CYAN}{subtype.getName()}{color.RESET} is not in {type}")
            else :
                print(f"{color.RED}Error : {color.CYAN}{type.getName()}{color.RESET} is not in DataPerson")

    def removePerson(self, id) :
        person = self.getPerson(id) #Print Error
        if person != None :
            type, subtype = person.getTypage()
            del self.__person[id]
            print(f"Person {color.BLUE}{id}{color.RESET} has been removed from DataPerson")
            self.getType(type).getSubtype(subtype).removeLinkPlace(id)

    def addTypePerson(self, name) :
        if name in self.getTypes() :
            print(f"{color.RED}Error :{color.RESET} Type {color.BLUE}{type}{color.RESET} is already in DataPerson")
        else :
            self.__type[name] = self.TypePerson(name)
            print(f"Type {color.CYAN}{name}{color.RESET} has been added to DataPerson")

    def removeTypePerson(self, name=None, select=False) :
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
                if len(type.getSubtype(subtypes[subtype]).getPeople()) > 0 :
                    full = True
                subtype += 1
            if full == False :
                del self.__type[name]
                print(f"Type {color.CYAN}{type.getName()}{color.RESET} has been removed from DataPerson")
            else :
                print(f"{color.RED}Error :{color.RESET} Type {color.CYAN}{type.getName()}{color.RESET} still contains people")

    def countPerson(self, show=True) :
        l = list()
        sum = 0
        for type in self.getTypes() :
            count = self.getType(type).countPlace(show=False)
            l.extend(count)
            sum += count[-1][-1]
        l.insert(0, ["DataPerson", "Total", sum])
        if show == True :
            print(f"Total {color.CYAN}{l[0][0].upper()}{color.RESET} : {l[0][2]} people\n_________________________")
            for elem in l[1:] :
                if elem[1] == "Total" :
                    print(f"Total {color.CYAN}{elem[0].upper()}{color.RESET} : {elem[2]} people")
                else :
                    print(f"  {color.CYAN}{elem[1]}{color.RESET} : {elem[2]} people")
        return l

    def countKnownState(self, infection, states, check=False, show=True) :
        if check == False :
            datainfection = DataInfection.DataInfection()
            infection = datainfection.getInfection(infection) #Print Error
            if infection != None :
                states = infection.__validStates(states) #Print Error
                if states != None :
                    check = True
        if check == True :
            l = list()
            sum = 0
            if len(self.getTypes()) > 0 :
                for type in self.getTypes() :
                    count = self.getType(type).countKnownState(infection=infection, states = states, check=True, show=False)
                    l.extend(count)
                    sum += count[-1][-1]
            l.insert(0, ["DataPerson", "Total", sum])
            if show == True :
                print(f"Total {color.CYAN}{l[0][0].upper()}{color.RESET} : {l[0][2]} people\n_________________________")
                for elem in l[1:] :
                    if elem[1] == "Total" :
                        print(f"Total {color.CYAN}{elem[0].upper()}{color.RESET} : {elem[2]} people")
                    else :
                        print(f"  {color.CYAN}{elem[1]}{color.RESET} : {elem[2]} people")
        return l

    def countRealState(self, infection, states, check=False, show=True) :
        if check == False :
            datainfection = DataInfection.DataInfection()
            infection = datainfection.getInfection(infection) #Print Error
            if infection != None :
                states = infection.__validStates(states) #Print Error
                if states != None :
                    check = True
        if check == True :
            state = self.__checkStates()
            if len(state)==0 :
                state = self.__getStates()
            l = list()
            sum = 0
            if len(self.getTypes()) > 0 :
                for type in self.getTypes() :
                    count = self.getType(type).countRealState(infection=infection, states = states, check=True, show=False)
                    l += count
                    sum += count[-1][-1]
            l.insert(0, ["DataPerson", "Total", sum])
            if show == True :
                print(f"Total {color.CYAN}{l[0][0].upper()}{color.RESET} : {l[0][2]} people\n_________________________")
                for elem in l[1:] :
                    if elem[1] == "Total" :
                        print(f"Total {color.CYAN}{elem[0].upper()}{color.RESET} : {elem[2]} people")
                    else :
                        print(f"  {color.CYAN}{elem[1]}{color.RESET} : {elem[2]} people")
        return l

    def __str__(self) :
        kwargs = dict()
        kwargs["indent"] = 1
        kwargs["typage"] = kwargs.get("typage", True)
        kwargs["type"] = kwargs.get("type", True)
        kwargs["person"] = kwargs.get("person", False)
        kwargs["limit"] = kwargs.get("limit", 5)

        string = f"{color.UNDERLINE}DataPerson :{color.RESET}"
        for type in self.getTypes() :
            string += f"\n\n{self.getType(type).__str__(**kwargs)}"
        return string

    def __repr__(self) :
        return self.__str__()


    class TypePerson() :

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
            if name in self.getSubtypes():
                return self.__subtype[name]
            else :
                print(f"{color.RED}Error :{color.RESET} Subtype {color.CYAN}{name}{color.RESET} is not in type {self.getName()}")
                return None

        def getPeople(self) :
            l = list()
            for subtype in self.getSubtypes() :
                l.extend(self.getSubtype(subtype).getPeople())
            return l

        def addSubtypePerson(self, name) :
            if name in self.getSubtypes() :
                print(f"{color.RED}Error :{color.RESET} Subtype {color.CYAN}{name}{color.RESET} is already in type {self.getName()}")
            else :
                self.__subtype[name] = self.SubtypePerson(name, self.getName())
                print(f"Subtype {color.CYAN}{name}{color.RESET} has been added to type {self.getName()}")

        def removeSubtypePerson(self, name=None, select=False) :
            subtype = getSubtype(name) #Print Error
            if subtype == None :
                if select == True :
                    for subtype in self.getSubtypes() :
                        print(subtype)
                    name = input(f"{color.GREEN}Select subtype name to remove :{color.RESET}")
                    subtype = getSubtype(name) #Print Error
            if subtype != None :
                if len(subtype.getPeople()) == 0 :
                    del self.__subtype[name]
                    print(f"Subtype {color.CYAN}{subtype.getName()}{color.RESET} has been removed from type {self.getName()}")
                else :
                    print(f"{color.RED}Error :{color.RESET} Type {color.CYAN}{subtype.getName()}{color.RESET} still contains people")

        def countPerson(self, show=True) :
            l = list()
            sum = 0
            if len(self.getSubtypes()) > 0 :
                for subtype in self.getSubtypes() :
                    count = self.getSubtype(subtype).countPerson(show=False)
                    l.extend(count)
                    sum += count[-1][-1]
            l.append([self.getName(), "Total", sum])
            if show == True :
                for elem in l :
                    if elem[1] == "Total" :
                        print(f"Total {color.CYAN}{elem[0].upper()}{color.RESET} : {elem[2]} people")
                    else :
                        print(f"  {color.CYAN}{elem[1]}{color.RESET} : {elem[2]} people")
            return l

        def countKnownState(self, infection, states, check=False, show=True) :
            if check == False :
                datainfection = DataInfection.DataInfection()
                infection = datainfection.getInfection(infection) #Print Error
                if infection != None :
                    states = infection.__validStates(states) #Print Error
                    if states != None :
                        check = True
            if check == True :
                l = list()
                sum = 0
                if len(self.getSubtypes()) > 0 :
                    for subtype in self.getSubtypes() :
                        count = self.getSubtype(subtype).countKnownState(infection=infection, states=states, check=True, show=False)
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

        def countRealState(self, infection, states, show=True) :
            if check == False :
                datainfection = DataInfection.DataInfection()
                infection = datainfection.getInfection(infection) #Print Error
                if infection != None :
                    states = infection.__validStates(states) #Print Error
                    if states != None :
                        check = True
            if check == True :
                l = list()
                sum = 0
                if len(self.getSubtypes()) > 0 :
                    for subtype in self.getSubtypes() :
                        count = self.getSubtype(subtype).countRealState(infection=infection, states=states, check=True, show=False)
                        l += count
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
            kwargs["indent"] = indent + 1
            kwargs["typage"] = kwargs.get("typage", True)
            kwargs["type"] = kwargs.get("type", False)
            kwargs["person"] = kwargs.get("person", False)
            kwargs["limit"] = kwargs.get("limit", 10)

            string = "\t"*indent + f"{color.UNDERLINE}Type :{color.RESET} {color.CYAN}{self.getName()}{color.RESET}"
            for subtype in self.getSubtypes() :
                string += f"\n\n{self.getSubtype(subtype).__str__(**kwargs)}"
            return string

        def __repr__(self) :
            return self.__str__()


        class SubtypePerson () :
            def __init__(self, name, type):
                self.__feature = dict()
                self.__person=list()
                self.__name = str(name)
                self.__type = str(type)

            def getName(self) :
                return self.__name

            def getType(self) :
                return self.__type

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

            def getPeople(self) :
                return self.__person

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

            def addPerson(self, age, id=None, autoId=None, **kwargs) :
                DataPerson().addPerson(id=id, autoId=autoId, age=age, type=self.getType(), subtype=self.getName(), **kwargs)

            def addLinkPerson(self, id) :
                person = DataPerson().getPerson(id) # Print Error
                if person != None :
                    type, subtype = person.getTypage()
                    if type == self.getType() and subtype == self.getName() :
                        if id in self.getPeople() :
                            print(f"{color.RED}Error :{color.RESET} Person {color.BLUE}{id}{color.RESET} is already in typage : {self.getType()} | {self.getName()}")
                        else :
                            self.__person.append(id)
                            print(f"Person {color.BLUE}{id}{color.RESET} has been added to typage : {self.getType()} | {self.getName()}")
                    else :
                        print(f"{color.RED}Error :{color.RESET} Person {color.BLUE}{id}{color.RESET} is link to an other typage : {type} | {subtype}")

            def removeLinkPerson(self, id) :
                if id in DataPerson().getPeople() :
                    print(f"{color.RED}Error :{color.RESET} Person {color.BLUE}{id}{color.RESET} is still in DataPerson")
                else :
                    if id in self.getPeople() :
                        self.__person.remove(id)
                        print(f"Person {color.BLUE}{id}{color.RESET} has been removed from typage : {self.getType()} | {self.getName()}")
                    else :
                        print(f"{color.RED}Error :{color.RESET} Person {color.BLUE}{id}{color.RESET} is no longer linked to typage : {self.getType()} | {self.getName()}")

            def countPerson(self, show=True):
                l = list()
                l.append([self.getType(), self.getName(), len(self.getPeople())])
                if show == True :
                    print(f"  {color.CYAN}{l[0][1]}{color.RESET} : {l[0][2]} people")
                return l

            def countKnownState(self, infection, states, check=False, show=True) :
                if check == False :
                    datainfection = DataInfection.DataInfection()
                    infection = datainfection.getInfection(infection) #Print Error
                    if infection != None :
                        states = infection.__validStates(states) #Print Error
                        if states != None :
                            check = True
                if check == True :
                    dataperson = DataPerson()
                    l = list()
                    sum = 0
                    for person in self.getPeople() :
                        if dataperson.getPerson(person).getKnownState(infection) in states :
                            sum += 1
                    l.append([self.getType(), self.getName(), sum])
                    if show == True :
                        print(f"  {color.CYAN}{l[0][1]}{color.RESET} : {l[0][2]} people")
                return l

            def countRealState(self, infection, states, check=False, show=True) :
                if check == False :
                    datainfection = DataInfection.DataInfection()
                    infection = datainfection.getInfection(infection) #Print Error
                    if infection != None :
                        states = infection.__validStates(states) #Print Error
                        if states != None :
                            check = True
                if check == True :
                    dataperson = DataPerson()
                    l = list()
                    sum = 0
                    for person in self.getPeople() :
                        if dataperson.getPerson(person).getRealState(infection) in states :
                            sum += 1
                    l.append([self.getType(), self.getName(), sum])
                    if show == True :
                        print(f"  {color.CYAN}{l[0][1]}{color.RESET} : {l[0][2]} people")
                return l

            def __str__(self, **kwargs) :
                indent = kwargs.get("indent", 0)
                kwargs["indent"] = indent + 1
                type = kwargs.get("type", True)
                person = kwargs.get("person", True)
                limit = kwargs.get("limit", 10)
                kwargs["typage"] = kwargs.get("typage", False)

                string = "\t"*indent + f"{color.UNDERLINE}Subtype :{color.RESET} {color.CYAN}{self.__name}{color.RESET}"
                if type == True :
                    string += f", from {color.CYAN}{self.__type}{color.RESET}"
                features = self.getFeatures()
                if len(features) > 0 :
                    string += "\n\t" + "\t"*indent + "Features :"
                    for feature in self.getFeatures() :
                        if isinstance(self.getFeature(feature), dict) :
                            dic = self.getFeature(feature)
                            for key, value in dic.items() :
                                string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{feature}{color.RESET} | {key} : {value}"
                        else :
                            string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{feature}{color.RESET} : {self.getFeature(feature)}"
                people = self.getPeople()
                if len(people) > 0 :
                    if len(people) < limit or limit == None :
                        size = len(people)
                    else :
                        size = limit
                    r = sample(people, size)
                    if person == False :
                        string += "\n\t" + "\t"*indent + "People :"
                        for id in r :
                            string += "\n\t\t" + "\t"*indent + f"{color.BLUE}{id}{color.RESET}"
                    else :
                        for id in r :
                            string += f"\n\n{DataPerson().getPerson(id).__str__(**kwargs)}"
                    if len(people) > limit :
                        string += "\n\t\t" + "\t"*indent + f"{color.BLUE}...{color.RESET}"

                return string

            def __repr__(self) :
                return self.__str__()


    class Person():
        def __init__(self, id, age, type, subtype, **kwargs):
            self.__typage = [str(type), str(subtype)]
            self.__id = id
            self.__age = age
            self.__infection = dict()
            self.__feature = dict()
            self.__script = dict()

        def getId(self) :
            return self.__id

        def getAge(self) :
            return self.__age

        def getTypage(self) :
            return self.__typage

        def getType(self) :
            return self.__typage[0]

        def getSubtype(self):
            return self.__typage[1]

        def getFeatures(self) :
            l = list()
            for key in self.__feature.keys():
                l.append(key)
            return l

        def getFeature(self, feature) :
            if feature in self.getFeatures() :
                return self.__feature[feature]
            else :
                print(f"{color.RED}Error :{color.RESET} Feature {color.CYAN}{feature}{color.RESET} is not in features")
                return None

        def getInfections(self) :
            l = list()
            for key in self.__infection.keys():
                l.append(key)
            return l

        def setInfection (self, infection, real, known, check=False) :
            if check == False :
                datainfection = DataInfection.DataInfection()
                infection = datainfection.getInfection(infection) #Print Error
                if infection != None :
                    real = infection.__validStates(real) #Print Error
                    known = infection.__validStates(known) #Print Error
                    if real != None and known != None :
                        check = True
            if check == True :
                self.__infection[infection] = [real, known]
                print(f"Person {self.getId()} has infection {color.CYAN}{infection}{color.RESET} with real state {real} and known state {known}")

        def getKnownState(self, infection) :
            if infection in self.getInfections() :
                return self.__infection[infection][1]
            else :
                print(f"{color.RED}Error :{color.RESET} Infection {color.CYAN}{infection}{color.RESET} is not initialized for person {self.getId()}")
                return None

        def getRealState(self, infection) :
            if infection in self.getInfections() :
                return self.__infection[infection][0]
            else :
                print(f"{color.RED}Error :{color.RESET} Infection {color.CYAN}{infection}{color.RESET} is not initialized for person {self.getId()}")
                return None

        def getDaysScript(self) :
            l = list()
            for key in self.__script.keys():
                l.append(key)
            return l

        def addScript(self, id, change=False) :
            datascript = DataScript.DataScript()
            if id in datascript.getScripts() :
                script = datascript.getScript(id)
                if script.getPerson() == self.getId() :
                    day = script.getDay()
                    if self.getDayScript(day) != None :
                        if change == False :
                            print(f"{color.RED}Error :{color.RESET} Script {color.BLUE}{self.getDayScript(day)}{color.RESET} has already been added to scripts with day {color.CYAN}{day}{color.RESET}")
                        else :
                            datascript.removeScript(self.getDayScript(day))
                            self.__script[day] = id
                            print(f"Script {color.BLUE}{self.getDayScript(day)}{color.RESET} has been removed to add {color.BLUE}{id}{color.RESET} to scripts with day {color.CYAN}{day}{color.RESET}")
                    else :
                        self.__script[day] = id
                        print(f"Script {color.BLUE}{id}{color.RESET} has been added to scripts with day {color.CYAN}{day}{color.RESET}")
                else :
                    print(f"{color.RED}Error : {color.RESET}Script {color.BLUE}{id}{color.RESET} is not associated to person {color.BLUE}{self.getId()}{color.RESET}")
            else :
                print(f"{color.RED}Error : {color.RESET}Script {color.BLUE}{id}{color.RESET} does not exist in scripts")

        def getDayScript(self, day) :
            if day in self.getDaysScript() :
                return self.__script[day]
            else :
                print(f"{color.RED}Error : {color.RESET}Day {color.CYAN}{day}{color.RESET} not in scripts")
                return None

        def removeScript(self, id) :
            datascript = DataScript.DataScript()
            if id in datascript.getScripts() :
                script = datascript.getScript(id)
                if script.getPerson() == self.getId() :
                    del self.__script[script.getDay()]
                    print(f"Script {color.BLUE}{id}{color.RESET} has been deleted from person {color.BLUE}{self.getId()}{color.RESET}")
                else :
                    print(f"{color.RED}Error : {color.RESET}Script {color.BLUE}{id}{color.RESET} is not associated to person {color.BLUE}{self.getId()}{color.RESET}")
            else :
                print(f"{color.RED}Error : {color.RESET}Script {color.BLUE}{id}{color.RESET} does not exist in scripts")

        def setKnownState(self, state) :
            if state in DataInfection.DataInfection().Infection("Covid").getStates() :
                print(f"{color.RED}Error : {color.CYAN}{state}{color.RESET} not in state")
            else :
                self.__known_state = state

        def setRealState(self, state) :
            if state in DataInfection.DataInfection().Infection("Covid").getStates() :
                print(f"{color.RED}Error : {color.CYAN}{state}{color.RESET} not in state")
            else :
                self.__real_state = state

        # !!
        def changeTypage(self) :
            print(f"{color.RED}Error : {color.RESET}Function to define ...")

        def addFeature(self, feature, value, change=False):
            if feature in self.getFeatures() :
                print(f"{color.RED}Error : {color.CYAN}{feature}{color.RESET} already in features with value : {self.getFeature(feature)}")
                if change == True :
                    self.__feature[feature] = value
                    print(f"Value of feature {color.CYAN}{feature}{color.RESET} has been changed")
            else :
                self.__feature[feature] = value
                print(f"Feature {color.CYAN}{feature}{color.RESET} has been added")

        def removeFeature(self, feature=None, select=False) :
            if feature not in self.getFeatures():
                if feature != None :
                    print(f"{color.RED}Error : {color.CYAN}{feature}{color.RESET} not in features")
                if select == True :
                    for feature in self.getFeatures() :
                        print(f"{color.CYAN}{feature}{color.RESET} : {self.getFeature(feature)}")
                    feature = input("\n-- Select item feature to delete : ")
            if feature in self.getFeatures() :
                del self.__feature[feature]
                print(f"Feature {color.CYAN}{feature}{color.RESET} has been deleted from features")

        def __str__(self, **kwargs) :
            indent = kwargs.get("indent", 0)
            typage = kwargs.get("typage", True)

            string = "\t"*indent + f"{color.UNDERLINE}Place :{color.BLUE}{self.getId()}{color.RESET}"
            if typage == True :
                string += "\n\t" + "\t"*indent + f"type : {color.CYAN}{self.getType()}{color.RESET}"
                string += "\n\t" + "\t"*indent + f"subtype : {color.CYAN}{self.getSubtype()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"age : {color.CYAN}{self.getAge()}{color.RESET}"
            """
            string += "\n\t" + "\t"*indent + f"known state : {color.CYAN}{self.getKnownState()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"real state : {color.CYAN}{self.getRealState()}{color.RESET}"
            features = self.getFeatures()
            if len(features)>0 :
                string += "\n\t" + "\t"*indent + "Features :"
                for feature in features :
                    if type(self.getFeature(feature)) == dict :
                        dic = self.getFeature(feature)
                        for key, value in dic.items():
                            string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{feature}{color.RESET} | {key} : {value}"
                        else :
                            string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{feature}{color.RESET} : {self.getFeature(feature)}"
            scripts = self.getScripts()
            if len(scripts)>0:
                string += "\n\t" + "\t"*indent + "Scripts :"
                for script in scripts :
                    string += "\n\t\t" + "\t"*indent + f"{color.CYAN}{script}{color.RESET} : {self.getScript(script)}"
            """
            return string

        def __repr__(self) :
            return self.__str__(typage=True)
'''