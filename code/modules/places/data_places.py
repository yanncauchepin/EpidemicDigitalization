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
            'nodes' : self.place[7],
            'tags' : self.place[8]
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

    def get_place(self, id_key):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Places WHERE id = ? ",
                            (id_key,))
        id_place = self.cursor.fetchone()
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
