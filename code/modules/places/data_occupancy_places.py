from modules.tools.singleton import Singleton
from modules.infections.data_infections import DataInfections
from modules.tools.style import Color
import os
import sqlite3


class SubOccupancy() :

    def __init__(self, suboccupancy):
        self.suboccupancy = suboccupancy

    def __getitem__(self, key) :
        values = {
            'start_time' : self.suboccupancy[0],
            'end_time' : self.suboccupancy[1],
            'individual_id' : self.suboccupancy[2],
            }
        if key in values.keys():
            return values[key]
        elif key in ['all', 'values']:
            return values
        else:
            raise KeyError(f"Key '{key}' not found.")
            

class OccupancyPlace():
    
    def __init__(self, occupancy_places):
        self.occupancy_places = occupancy_places 
    
    def __getitem__(self, key) :
        values = {
            "day" : self.occupancy_places[0],
            "place_id" : self.occupancy_places[1],
            "occupancy" : eval(self.occupancy_places[2])
            }
        if key in values.keys():
            return values[key]
        elif key in ['all', 'values']:
            return values
        else:
            raise KeyError(f"Key '{key}' not found.")


class DataOccupancyPlaces(metaclass=Singleton):
    
    def __init__(self, occupancy_places_database_path, dataplaces, raise_error_on_duplicate_id=False) :
        os.makedirs(os.path.dirname(occupancy_places_database_path), exist_ok=True) 
        self.occupancy_places_database_path = occupancy_places_database_path
        self.raise_error_on_duplicate_id = raise_error_on_duplicate_id
        self.dataplaces = dataplaces
        
    def __start_connection_db(self):
        self.connection = sqlite3.connect(self.occupancy_places_database_path)
        self.cursor = self.connection.cursor()
        
    def __end_connection_db(self):
        self.cursor.close()
        self.connection.close()
    
    def create_database(self) :
        self.__start_connection_db()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS OccupancyPlaces (
            place_id INTEGER,
            day INTEGER,
            occupancy TEXT,
            FOREIGN KEY (place_id) REFERENCES Places(id)
            )''')
        self.__end_connection_db()
        
    def insert_occupancy_places(self, day, place_id, occupancy='[]'):
        self.__start_connection_db()
        check_conditions = True
        # Check if infection_name exists in Infections
        existing_place = self.dataplaces.get_place(place_id)
        if not existing_place:
            check_conditions = False
            if self.raise_error_related_id_not_exists:
                raise ValueError(f"Place id {place_id} does not exist in "
                                 "the places database.")
            else:
                print(f"{Color.RED}Warning:{Color.RESET} Place id {place_id} "
                      "does not exist in the places database.")
        if check_conditions == True:
            # Insert the individual infection according to above conditions
            self.cursor.execute('''INSERT INTO OccupancyPlaces (
                day, place_id, occupancy
                ) VALUES (?, ?, ?)''',
                (day, place_id, occupancy))
            self.connection.commit()
        self.__end_connection_db()

    def assign_day_occupancy_to_place(self, day, place_id, occupancy):
        self.__start_connection_db()
        # Check if both id exists
        if not isinstance(occupancy, str):
            occupancy = str(occupancy)
        self.cursor.execute('''UPDATE OccupancyPlaces SET occupancy = ? WHERE day = ? AND place_id = ?''',
                            (occupancy, day, place_id))
        self.connection.commit()
        self.__end_connection_db()

    def remove_occupancy_places(self, day, place_id):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM OccupancyPlaces WHERE day = ? "
                            "AND place_id = ?", 
                            (day,place_id))
        self.connection.commit()
        self.__end_connection_db()
        
    def reset_database(self):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM OccupancyPlaces")
        self.connection.commit()
        self.__end_connection_db()

    def end_connection_db(self):
        self.__start_connection_db()
        self.cursor.close()
        self.connection.close()
        self.__end_connection_db()
        
    """Get individual infections"""
        
    def get_all_occupancy_places_by_day(self, day):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM OccupancyPlaces WHERE day = ? ", 
                            (day,))
        all_occupancy_places = self.cursor.fetchall()
        self.__end_connection_db()
        return all_occupancy_places
    
    def get_day_occupancy_place(self, day, place_id):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM OccupancyPlaces WHERE day = ? AND place_id = ?", 
                            (day, place_id))
        occupancy_place = self.cursor.fetchall()
        self.__end_connection_db()
        return occupancy_place
    
    """Count individual infections"""
    
    def count_occupancy_places(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM OccupancyPlaces")
        count_all = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_all
    
    def count_occupancy_places_by_day(self, name):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM OccupancyPlaces WHERE day = ?", 
                            (day,))
        count_day_occupancy_places = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_day_occupancy_places