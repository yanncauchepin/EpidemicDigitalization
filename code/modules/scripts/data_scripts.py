from modules.tools.singleton import Singleton
from modules.tools.style import Color
import os
import sqlite3

class Trip():
    
    def __init__(self, trip):
        self.trip = trip
    
    def __getitem__(self, key) :
        values = {
            'place_id' : self.trip[0],
            'start_time' : self.trip[1],
            'end_time' : self.trip[2],
            }
        if key in values.keys():
            return values[key]
        elif key in ['all', 'values']:
            return values
        else:
            raise KeyError(f"Key '{key}' not found.")

class Script():
    
    def __init__(self, script):
        self.script = script
    
    def __getitem__(self, key) :
        values = {
            'day' : self.script[0],
            'individual_id' : self.script[1],
            'type' : self.script[2],
            'sequence' : eval(self.script[3]),
            'bool_computed_trips_duration' : self.script[4],
            'tags' : self.script[5]
            }
        if key in values.keys():
            return values[key]
        elif key in ['all', 'values']:
            return values
        else:
            raise KeyError(f"Key '{key}' not found.")


class DataScripts(metaclass=Singleton):
    
    def __init__(self, database_path, dataindividuals, raise_error_on_duplicate_id=False,
                 raise_error_related_id_not_exists=False) :
        os.makedirs(os.path.dirname(database_path), exist_ok=True)
        self.database_path = database_path
        self.raise_error_on_duplicate_id = raise_error_on_duplicate_id
        self.raise_error_related_id_not_exists = raise_error_related_id_not_exists
        self.dataindividuals = dataindividuals
        
    def __start_connection_db(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        
    def __end_connection_db(self):
        self.cursor.close()
        self.connection.close()
    
    def create_database(self) :
        self.__start_connection_db()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Scripts (
            day INTEGER,
            individual_id INTEGER,
            type TEXT,
            sequence TEXT,
            bool_computed_trips_duration INTEGER,
            tags TEXT,
            PRIMARY KEY (day, individual_id)
            )''')
        self.__end_connection_db()
        
    def insert_script(self, day, individual_id, type_name, sequence="[]", 
                      bool_computed_trips_duration=0, tags="None"):
        self.__start_connection_db()
        
        check_conditions = True
        # Check if infection_name exists in Infections
        existing_individual = self.dataindividuals.get_individual(individual_id)
        if not existing_individual:
            check_conditions = False
            if self.raise_error_related_id_not_exists:
                raise ValueError(f"Individual with id {individual_id} does not "
                                 "exist in the individuals database.")
            else:
                print(f"{Color.RED}Warning:{Color.RESET} Individual with ID "
                      f"{individual_id} does not exist in the individuals database.")
        if check_conditions == True:
            # Insert the sript
            self.cursor.execute('''INSERT INTO Scripts (
                day, individual_id, type, sequence, bool_computed_trips_duration, tags
                ) VALUES (?, ?, ?, ?, ?, ?)''',
            (day, individual_id, type_name, sequence, bool_computed_trips_duration, tags))
            self.connection.commit()
        self.__end_connection_db()
            
    def assign_sequence_to_individual_day_script(self, day, individual_id, sequence):
        self.__start_connection_db()
        # Check if both id exists
        if not isinstance(sequence, str):
            sequence = str(sequence)
        self.cursor.execute('''UPDATE Scripts SET sequence = ? WHERE day = ? 
                            AND individual_id = ?''',
                            (sequence, day, individual_id))
        self.connection.commit()
        self.__end_connection_db()
        
    def assign_bool_computed_trips_duration_to_individual_day_script(self, day, individual_id, 
                                                                    transport_duration_computed):
        self.__start_connection_db()
        # Check if both id exists
        self.cursor.execute('''UPDATE Scripts SET transport_duration_computed = ? WHERE day = ? 
                            AND individual_id = ?''',
                            (transport_duration_computed, day, individual_id))
        self.connection.commit()
        self.__end_connection_db()

    def remove_script(self, day, individual_id):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM Scripts WHERE day = ? AND individual_id = ?", 
                            (day, individual_id))
        self.connection.commit()
        self.__end_connection_db()
        
    def reset_database(self):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM Scripts")
        self.connection.commit()
        self.__end_connection_db()

    """Get scripts"""
    
    def get_day_scripts(self, day):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Scripts WHERE day = ?", 
                            (day,))
        day_scripts = self.cursor.fetchall()
        self.__end_connection_db()
        return day_scripts
    
    def get_individual_scripts(self, individual_id):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Scripts WHERE individual_id = ?", 
                            (individual_id,))
        individual_scripts = self.cursor.fetchall()
        self.__end_connection_db()
        return individual_scripts

    def get_individual_day_script(self, day, individual_id):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Scripts WHERE day = ? AND individual_id = ?", 
                            (day, individual_id))
        individual_day_script = self.cursor.fetchone()
        self.__end_connection_db()
        return individual_day_script
    
    """Count scripts"""
    
    def count_scripts(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM Scripts")
        count_all = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_all
    
    def count_scripts_by_day(self, day):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM Scripts WHERE day = ?", 
                            (day,))
        count_day = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_day


'''----------------------------------------------------------------> DEPRECATED


from Modules.Person import DataPerson
from Modules.Place import DataPlace
from Modules.Script import setScript
from Modules.Tools import Singleton
from Modules.Tools.Style import color

class DataScript (metaclass=Singleton.Singleton):
    __nextIdScript = 1

    def __init__(self):
        self.__script=dict()

    def __incrementScript(self):
        self.__nextIdScript += 1

    def __getIdScript(self):
        return self.__nextIdScript

    def getScripts(self) :
        l = list()
        for key in self.__script.keys():
            l.append(key)
        return l

    def getScript(self, script) :
        if script not in self.getScripts():
            print(f"\n{color.RED}Error : {color.BLUE}{script}{color.RESET} not in scripts")
            return None
        else :
            return self.__script[script]

    def addScript(self, person, day, type=None, **kwargs) :
        dataperson = DataPerson.DataPerson()
        id = self.__getIdScript()
        while id in self.getScripts():
            self.__incrementScript()
            id = self.__getIdScript()
        if person in dataperson.getPeople() :
            self.__script[id] = self.Script (id, person, day, type=type, **kwargs)
            print(f"Script {color.BLUE}{id}{color.RESET} has been added to scripts")
            dataperson.getPerson(person).addScript(id, change=True)
            return id
        else :
            print(f"{color.RED}Error : {color.CYAN}{type}{color.RESET} not in types")
            return None

    def removeScript(self, id) :
        dataperson = DataPerson.DataPerson()
        if id in DataScript().getScripts() :
            del self.__script[id]
            print(f"Script {color.BLUE}{id}{color.RESET} has been deleted from scripts")
        else :
            print(f"{color.RED}Error : {color.BLUE}{id}{color.RESET} not in scripts" )

    def __str__(self) :
        kwargs = dict()
        kwargs["indent"]=1
        string = f"{color.UNDERLINE}DataScript :{color.RESET}"
        for script in self.getScripts() :
            string += f"\n\n{self.getScript(script).__str__(**kwargs)}"
        return string

    def __repr__(self):
        return self.__str__()

    class Script ():
        def __init__(self, id, person, day, type=None, **kwargs):
            self.__id = id
            self.__person = person
            self.__day = day
            if setScript.checkTypeScript(type) :
                self.__sequence = setScript.applyTypeScript(type, person, day, **kwargs)
            else :
                self.__sequence = setSequence(type=None, select=True, change=False)

        def getId(self) :
            return self.__id

        def getPerson(self) :
            return self.__person

        def getDay(self) :
            return self.__day

        def getSequence(self) :
            return self.__sequence

        def setSequence(self, type=None, select=False, change=False, **kwargs) :
            if not setScript.checkTypeScript(type) :
                if select == None :
                    print(f"{color.RED}Error : {color.RESET}No sequence referenced" )
                else :
                    type = setScript.selectTypeScript()
            if setScript.checkTypeScript(type) :
                if self.getSequence() != None :
                    if change==True :
                        self.__sequence = setScript.applyTypeScript(type, self.getPerson(), self.getDay(), **kwargs)
                    else :
                        print(f"{color.RED}Error : {color.RESET}A sequence has already been set" )
                else :
                    self.__sequence = setScript.applyTypeScript(type, self.getPerson(), self.getDay(), **kwargs)

        def __str__(self, **kwargs) :
            indent = kwargs.get("indent", 0)
            string = "\t"*indent + f"{color.UNDERLINE}Script :{color.RESET} {color.BLUE}{self.getId()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"person : {color.CYAN}{self.getPerson()}{color.RESET}"
            string += "\n\t" + "\t"*indent + f"day : {color.CYAN}{self.getDay()}{color.RESET}"
            sequence = self.getSequence()
            if sequence != None :
                string += "\n\t" + "\t"*indent + "Sequence :"
                for elem in sequence :
                    string += "\n\t\t" + "\t"*indent + f"{elem}"
            return string

        def __repr__(self):
            return self.__str__()
        
'''
