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

    def get_individual(self, id_key):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Individuals WHERE id = ? ",
                            (id_key,))
        id_individual = self.cursor.fetchone()
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
