from modules.tools.singleton import Singleton
from modules.tools.style import Color
import os
import sqlite3


class Infection():

    def __init__(self, infection):
        self.infection = infection

    def __getitem__(self, key) :
        values = {
            "name" : self.infection[0],
            "individual_cumulative_days" : self.infection[1],
            "place_cumulative_minutes" : self.infection[2],
            "contamination_threshold" : self.infection[3],
            "mean_gaussian_incubation" : self.infection[4],
            "std_gaussian_incubation" : self.infection[5],
            "mean_gaussian_infection" : self.infection[6],
            "std_gaussian_infection" : self.infection[7],
            "lower_threshold" : self.infection[8],
            "upper_threshold" : self.infection[9],
            "incubation_emission" : self.infection[10],
            "asymptomatic_emission" : self.infection[11],
            "standard_emission" : self.infection[12],
            "serious_emission" : self.infection[13],
            "asymptomatic_healing" : self.infection[14],
            "standard_healing" : self.infection[15],
            "serious_aggravation" : self.infection[16],
            "death_threshold" : self.infection[17]
            }
        if key in values.keys():
            return values[key]
        elif key in ['all', 'values']:
            return values
        else:
            raise KeyError(f"Key '{key}' not found.")


class DataInfections(metaclass=Singleton):

    @property
    def contaminated_states(self):
        return ("E", "A", "I-", "I+")

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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Infections (
            name TEXT PRIMARY KEY,
            individual_cumulative_days INTEGER,
            place_cumulative_minutes INTEGER,
            contamination_threshold REAL,
            mean_gaussian_incubation REAL,
            std_gaussian_incubation REAL,
            mean_gaussian_infection REAL,
            std_gaussian_infection REAL,
            lower_threshold REAL,
            upper_threshold REAL,
            incubation_emission REAL,
            asymptomatic_emission REAL,
            standard_emission REAL,
            serious_emission REAL,
            asymptomatic_healing REAL,
            standard_healing REAL,
            serious_aggravation REAL,
            death_threshold REAL
            )''')
        self.__end_connection_db()

    def insert_infection(self, name, **params):
        self.__start_connection_db()
        # Check if the name already exists
        self.cursor.execute("SELECT name FROM Infections WHERE name = ?",
                            (name,))
        existing_name = self.cursor.fetchone()
        if existing_name:
            if self.raise_error_on_duplicate_id:
                raise ValueError(f"ID {name} already exists in the infections "
                                 "database.\n")
            else:
                print(f"{Color.RED}Warning:{Color.RESET} ID {name} already "
                      "exists in the infections database.\n")
        else:
            individual_cumulative_days = params.get("individual_cumulative_days", 4)
            place_cumulative_minutes = params.get("place_cumulative_minutes", 160)
            contamination_threshold = params.get("contamination_threshold", 250000)
            mean_gaussian_incubation = params.get("mean_gaussian_incubation", 8)
            std_gaussian_incubation = params.get("std_gaussian_incubation", 2)
            mean_gaussian_infection = params.get("mean_gaussian_infection", 100)
            std_gaussian_infection = params.get("std_gaussian_infection", 20)
            lower_threshold = params.get("lower_threshold", 80)
            upper_threshold = params.get("upper_threshold", 130)
            incubation_emission = params.get("incubation_emission", 1)
            asymptomatic_emission = params.get("asymptomatic_emission", 1)
            standard_emission = params.get("standard_emission", 1)
            serious_emission = params.get("serious_emission", 1)
            asymptomatic_healing = params.get("asymptomatic_healing", 5)
            standard_healing = params.get("standard_healing", 5)
            serious_aggravation = params.get("serious_aggravation", 3)
            death_threshold = params.get("death_threshold", 160)
            # Insert the place
            self.cursor.execute('''INSERT INTO Infections (
                name, individual_cumulative_days, place_cumulative_minutes,
                contamination_threshold, mean_gaussian_incubation,
                std_gaussian_incubation, mean_gaussian_infection,
                std_gaussian_infection, lower_threshold, upper_threshold,
                incubation_emission, asymptomatic_emission, standard_emission,
                serious_emission, asymptomatic_healing, standard_healing,
                serious_aggravation, death_threshold
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, individual_cumulative_days, place_cumulative_minutes,
            contamination_threshold, mean_gaussian_incubation,
            std_gaussian_incubation, mean_gaussian_infection,
            std_gaussian_infection, lower_threshold, upper_threshold,
            incubation_emission, asymptomatic_emission, standard_emission,
            serious_emission, asymptomatic_healing, standard_healing,
            serious_aggravation, death_threshold))
            self.connection.commit()
        self.__end_connection_db()

    def remove_infection(self, name):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM Infections WHERE name = ?",
                            (name,))
        self.connection.commit()
        self.__end_connection_db()

    def reset_database(self):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM Infections")
        self.connection.commit()
        self.__end_connection_db()

    def end_connection_db(self):
        self.__start_connection_db()
        self.cursor.close()
        self.connection.close()
        self.__end_connection_db()

    def get_all_infections(self) :
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Infections")
        all_infections = self.cursor.fetchall()
        self.__end_connection_db()
        return all_infections

    def get_infection(self, name):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM Infections WHERE name = ? ",
                            (name,))
        infection = self.cursor.fetchone()
        self.__end_connection_db()
        return infection

    def list_all_names(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT name FROM Infections")
        all_names = [row[0] for row in self.cursor.fetchall()]
        self.__end_connection_db()
        return all_names

    def count_infections(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM Infections")
        count_all = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_all
