from modules.tools.singleton import Singleton
from modules.infections.data_infections import DataInfections
from modules.tools.style import Color
import os
import sqlite3


class IndividualInfection():
    
    def __init__(self, individual_infection):
        self.individual_infection = individual_infection 
    
    def __getitem__(self, key) :
        values = {
            "infection_name" : self.individual_infection[0],
            "individual_id" : self.individual_infection[1],
            "real_state" : self.individual_infection[2],
            "known_state" : self.individual_infection[3],
            "contamination_score" : self.individual_infection[4],
            "incubation_duration" : self.individual_infection[5],
            "infection_start" : self.individual_infection[6],
            "infection_score" : self.individual_infection[7],
            "emission" : self.individual_infection[8],
            "immune_reaction" : self.individual_infection[9],
            "infection_end" : self.individual_infection[10]
            }
        if key in values.keys():
            return values[key]
        elif key in ['all', 'values']:
            return values
        else:
            raise KeyError(f"Key '{key}' not found.")


class DataIndividualInfections(metaclass=Singleton):
    
    def __init__(self, individual_infections_database_path, dataindividuals,
                 datainfections, raise_error_on_duplicate_id=False, 
                 raise_error_related_id_not_exists=False) :
        os.makedirs(os.path.dirname(individual_infections_database_path), exist_ok=True) 
        self.individual_infections_database_path = individual_infections_database_path
        self.raise_error_on_duplicate_id = raise_error_on_duplicate_id
        self.dataindividuals = dataindividuals
        self.datainfections = datainfections
        
    def __start_connection_db(self):
        self.connection = sqlite3.connect(self.individual_infections_database_path)
        self.cursor = self.connection.cursor()
        
    def __end_connection_db(self):
        self.cursor.close()
        self.connection.close()
    
    def create_database(self) :
        self.__start_connection_db()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS IndividualInfections (
            infection_name TEXT,
            individual_id INTEGER,
            real_state TEXT,
            known_state TEXT,
            contamination_score REAL,
            incubation_duration INTEGER,
            infection_start INTEGER,
            infection_score REAL,
            emission REAL,
            immune_reaction REAL,
            infection_end INTEGER,
            FOREIGN KEY (infection_name) REFERENCES Infections(name),
            FOREIGN KEY (individual_id) REFERENCES Individuals(id)
            )''')
        self.__end_connection_db()
        
    def insert_individual_infection(self, infection_name, individual_id, real_state='S', 
                                    known_state='S', contamination_score='[]', 
                                    incubation_duration=None, infection_start=None,
                                    infection_score=None, emission=None, 
                                    immune_reaction=None, infection_end=None):
        self.__start_connection_db()
        check_conditions = True
        # Check if infection_name exists in Infections
        existing_infection = self.datainfections.get_infection(infection_name)
        if not existing_infection:
            check_conditions = False
            if self.raise_error_related_id_not_exists:
                raise ValueError(f"Infection {infection_name} does not exist in "
                                 "the infections database.")
            else:
                print(f"{Color.RED}Warning:{Color.RESET} Infection {infection_name} "
                      "does not exist in the infections database.")
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
            # Insert the individual infection according to above conditions
            self.cursor.execute('''INSERT INTO IndividualInfections (
                infection_name, individual_id, real_state, known_state, contamination_score,
                incubation_duration, infection_start, infection_score, emission, immune_reaction,
                infection_end
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (infection_name, individual_id, real_state, known_state, contamination_score,
                incubation_duration, infection_start, infection_score, emission, immune_reaction,
                infection_end))
            self.connection.commit()
        self.__end_connection_db()
        
        
    def assign_real_state_to_individual_infection(self, infection_name, individual_id, real_state):
        self.__start_connection_db()
        self.cursor.execute('''UPDATE IndividualInfections SET real_state = ? WHERE infection_name = ? 
                            AND individual_id = ?''',
                            (real_state, infection_name, individual_id))
        self.connection.commit()
        self.__end_connection_db()
        
    def assign_known_state_to_individual_infection(self, infection_name, individual_id, known_state):
        self.__start_connection_db()
        self.cursor.execute('''UPDATE IndividualInfections SET known_state = ? WHERE infection_name = ? 
                            AND individual_id = ?''',
                            (known_state, infection_name, individual_id))
        self.connection.commit()
        self.__end_connection_db()

    def assign_contamination_score_to_individual_infection(self, infection_name, individual_id, contamination_score):
        self.__start_connection_db()
        self.cursor.execute('''UPDATE IndividualInfections SET contamination_score = ? WHERE infection_name = ? 
                            AND individual_id = ?''',
                            (contamination_score, infection_name, individual_id))
        self.connection.commit()
        self.__end_connection_db()
        
    def assign_incubation_duration_to_individual_infection(self, infection_name, individual_id, incubation_duration):
        self.__start_connection_db()
        self.cursor.execute('''UPDATE IndividualInfections SET incubation_duration = ? WHERE infection_name = ? 
                            AND individual_id = ?''',
                            (incubation_duration, infection_name, individual_id))
        self.connection.commit()
        self.__end_connection_db()

    def assign_infection_start_to_individual_infection(self, infection_name, individual_id, infection_start):
        self.__start_connection_db()
        self.cursor.execute('''UPDATE IndividualInfections SET infection_start = ? WHERE infection_name = ? 
                            AND individual_id = ?''',
                            (infection_start, infection_name, individual_id))
        self.connection.commit()
        self.__end_connection_db()
        
    def assign_infection_score_to_individual_infection(self, infection_name, individual_id, infection_score):
        self.__start_connection_db()
        self.cursor.execute('''UPDATE IndividualInfections SET infection_score = ? WHERE infection_name = ? 
                            AND individual_id = ?''',
                            (infection_score, infection_name, individual_id))
        self.connection.commit()
        self.__end_connection_db()
    
    def assign_emission_to_individual_infection(self, infection_name, individual_id, emission):
        self.__start_connection_db()
        self.cursor.execute('''UPDATE IndividualInfections SET emission = ? WHERE infection_name = ? 
                            AND individual_id = ?''',
                            (emission, infection_name, individual_id))
        self.connection.commit()
        self.__end_connection_db()
        
    def assign_immune_reaction_to_individual_infection(self, infection_name, individual_id, immune_reaction):
        self.__start_connection_db()
        self.cursor.execute('''UPDATE IndividualInfections SET immune_reaction = ? WHERE infection_name = ? 
                            AND individual_id = ?''',
                            (immune_reaction, infection_name, individual_id))
        self.connection.commit()
        self.__end_connection_db()
        
    def assign_infection_end_to_individual_infection(self, infection_name, individual_id, infection_end):
        self.__start_connection_db()
        self.cursor.execute('''UPDATE IndividualInfections SET infection_end = ? WHERE infection_name = ? 
                            AND individual_id = ?''',
                            (infection_end, infection_name, individual_id))
        self.connection.commit()
        self.__end_connection_db()

    def remove_individual_infection(self, infection_name, individual_id):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM IndividualInfections WHERE infection_name = ? "
                            "AND individual_id = ?", 
                            (infection_name,individual_id))
        self.connection.commit()
        self.__end_connection_db()
        
    def reset_database(self):
        self.__start_connection_db()
        self.cursor.execute("DELETE FROM IndividualInfections")
        self.connection.commit()
        self.__end_connection_db()

    def end_connection_db(self):
        self.__start_connection_db()
        self.cursor.close()
        self.connection.close()
        self.__end_connection_db()
        
    """Get individual infections"""
        
    def get_all_individuals_by_infection(self, infection_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM IndividualInfections WHERE infection_name = ? ", 
                            (infection_name,))
        all_individual_infections = self.cursor.fetchall()
        self.__end_connection_db()
        return all_individual_infections
    
    def get_individual_infection(self, infection_name, individual_id):
        self.__start_connection_db()
        self.cursor.execute("SELECT * FROM IndividualInfections WHERE infection_name = ? AND individual_id = ?", 
                            (infection_name, individual_id))
        indivual_infection = self.cursor.fetchall()
        self.__end_connection_db()
        return indivual_infection
    
    """List individual infections"""
    
    def list_all_individuals_by_infection(self, infection_name):
        self.__start_connection_db()
        self.cursor.execute("SELECT individual_id FROM IndividualInfections WHERE infection_name = ? ", 
                            (infection_name,))
        individual_infections = self.cursor.fetchall()
        self.__end_connection_db()
        return individual_infections
    
    """Count individual infections"""
    
    def count_individual_infections(self):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM IndividualInfections")
        count_all = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_all
    
    def count_individual_infections_by_infection(self, name):
        self.__start_connection_db()
        self.cursor.execute("SELECT COUNT(*) FROM IndividualInfections WHERE infection_name = ?", 
                            (name,))
        count_infection = self.cursor.fetchone()[0]
        self.__end_connection_db()
        return count_infection
     
