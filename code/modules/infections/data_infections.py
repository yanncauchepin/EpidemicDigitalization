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




'''----------------------------------------------------------------> DEPRECATED

from Modules.Person import DataPerson
from Modules.Tools import Singleton
from Modules.Tools import Stats
from Modules.Tools.Style import color

STATES = ["S", "E", "A", "I-", "I+", "D", "R", "V"]

class DataInfection (metaclass=Singleton.Singleton) :
    __nextIdInfection = 1

    def __init__(self) :
        self.__infection = dict()
        self.__person_state = dict()

    def checkState(self, state) :
        if state in STATES :
            return state
        else :
            print(f"{color.RED}Error{color.RESET} State {color.CYAN}{state}{color.RESET} not in available states")
            return None

    def getInfections(self) :
        l = list()
        for key in self.__infection.keys() :
            l.append(key)
        return l

    def getInfection(self, name) :
        if name in self.getInfections() :
            return self.__infection[name]
        else :
            print(f"\n{color.RED}Error :{color.RESET} Infection {color.CYAN}{name}{color.RESET} is not in DataInfection")
            return None

    def addInfection(self, name, **kwargs) :
        if name in self.getInfections() :
            print(f"{color.RED}Error :{color.RESET} Infection {color.BLUE}{name}{color.RESET} is already in DataInfection")
        else :
            self.__infection[name] = self.Infection(name, **kwargs)
            print(f"Infection {color.CYAN}{name}{color.RESET} has been added to DataInfection")

    def removeInfection(self, name=None, select=False) :
        infection = self.getInfection(name) #Print Error
        if infection == None :
            if select == True :
                for infection in self.getInfections() :
                    print(infection)
                name = input(f"{color.GREEN}Select infection name to remove :{color.RESET}")
                infection = self.getInfection(name) #Print Error
        if infection != None :
            del self.__infection[name]
            print(f"Infection {color.CYAN}{name}{color.RESET} has been removed from DataInfection")

    def getPeopleStates(self) :
        l = list()
        for key in self.__person_state.keys():
            l.append(key)
        return l

    def getPersonState(self, infection, person) :
        if (infection, person) not in self.getPeopleStates():
            print(f"{color.RED}Error :{color.RESET} Person state {color.CYAN}{person}{color.RESET} for infection {color.CYAN}{infection}{color.RESET} is not in People States")
            return None
        else :
            return self.__person_state[(infection, person)]

    def addPersonState(self, infection, person, initial_state="S") :
        if (infection, person) in self.getPeopleStates() :
            print(f"{color.RED}Error :{color.RESET} Person state {color.BLUE}{person}{color.RESET} for infection {color.BLUE}{infection}{color.RESET} is already in People States")
        else :
            infection = self.getInfection(infection) #Print Error
            person = DataPerson.DataPerson().getPerson(person) #Print Error
            if infection != None and person != None :
                state = DataInfection().checkState(initial_state) #Print Error
                if state != None :
                    self.__person_state[(infection.getName(), person.getId())] = self.PersonState(infection, person, initial_state)
                    print(f"Person state {color.BLUE}{person.getId()}{color.RESET} for infection {color.BLUE}{infection.getName()}{color.RESET} has been added to People States")

    def removePersonState(self, infection, person) :
        person_state = self.getPersonState(infection, person) #Print Error
        if person_state != None :
            del self.__person_state[(infection, person)]
            print(f"Person state {color.BLUE}{person}{color.RESET} for infection {color.BLUE}{infection}{color.RESET} has been removed from People States")

    class Infection () :
        def __init__(self, name, **kwargs) :
            self.__name = name
            self.__days_cumul_person = kwargs.get("days_cumul_person", 4)
            self.__seconds_cumul_place = kwargs.get("seconds_cumul_place", 9600)
            self.__infection_threshold = kwargs.get("infection_threshold", 250000)
            self.__gauss_incubation = kwargs.get("gauss_infection", [8,2])
            self.__gauss_score = kwargs.get("gauss_score", [100,20])
            self.__inf_threshold = kwargs.get("inf_threshold", 80)
            self.__sup_threshold = kwargs.get("sup_threshold", 130)
            self.__emission_incubation = kwargs.get("emission_incubation", 1)
            self.__emission_asymptomatic = kwargs.get("emission_asymptomatic", 1)
            self.__healing_asymptomatic = kwargs.get("healing_asymptomatic", 5)
            self.__emission_standard = kwargs.get("emission_standard", 1)
            self.__healing_standard = kwargs.get("healing_standard", 5)
            self.__emission_serious = kwargs.get("emission_serious", 1)
            self.__aggravation_serious = kwargs.get("aggravation_serious", 2)
            self.__death_threshold = kwargs.get("death_threshold", 160)

        def getName(self) :
            return self.__name

        def getDaysCumulPerson(self) :
            return self.__days_cumul_person

        def getSecondsCumulPlace(self) :
            return self.__seconds_cumul_place

        def getInfectionThreshold(self) :
            return self.__infection_threshold

        def getGaussIncubation(self) :
            return self.__gauss_incubation

        def getGaussScore(self) :
            return self.__gauss_score

        def getInfThreshold(self) :
            return self.__inf_threshold

        def getSupThreshold(self) :
            return self.__sup_threshold

        def getEmissionIncubation(self) :
            return self.__emission_incubation

        def getEmissionAsymptomatic(self) :
            return self.__emission_asymptomatic

        def getHealingAsymptomatic(self) :
            return self.__healing_asymptomatic

        def getEmissionStandard(self) :
            return self.__emission_standard

        def getHealingStandard(self) :
            return self.__healing_standard

        def getEmissionSerious(self) :
            return self.__emission_serious

        def getAggravationSerious(self) :
            return self.__aggravation_serious

        def getDeathThreshold(self) :
            return self.__death_threshold

        def getDivisionPersonState(self) :
            dataperson = DataPerson.DataPerson()
            people = dataperson.getPeople()
            count = dict()
            for state in STATES :
                count[state] = 0
            for person in people :
                person_state = DataInfection().getPersonState(self.getName(), person)
                if person_state != None :
                    state = person_state.getRealState()
                    count[state] += 1
            return count

    class PersonState ():
        def __init__(self, infection_object, person_object, initial_state="S") :
            self.__infection = infection_object
            self.__person = person_object
            self.__known = "S"
            self.__real = None
            self.setState(initial_state)

        def getInfection(self) :
            return self.__infection

        def getPerson(self) :
            return self.__person

        def getAgePerson(self) :
            return self.__person.getAge()

        def getState(self) :
            return self.__real

        def getRealState(self, ) :
            return self.getState().getName()

        def setState(self, state, score=None) :
            state = DataInfection().checkState(state) #Print Error
            if state != None :
                infection = self.getInfection()
                #if self.getRealState() != state :
                    #del self.__real
                if state == "S" :
                    self.__real = self.Susceptible(infection.getDaysCumulPerson(), infection.getInfectionThreshold())
                elif state == "E" :
                    self.__real = self.Incubation(self.__assignDurationIncubation(), infection.getEmissionIncubation())
                elif state == "A" :
                    self.__real = self.Asymptomatic(score, infection.getEmissionAsymptomatic(), infection.getHealingAsymptomatic())
                elif state == "I-" :
                    self.__real = self.Standard(score, infection.getEmissionStandard(), infection.getHealingStandard(), infection.getSupThreshold())
                elif state == "I+" :
                    self.__real = self.Serious(score, infection.getEmissionSerious(), infection.getAggravationSerious(), infection.getDeathThreshold())
                    self.setKnownState("I+")
                elif state == "R" :
                    self.__real = self.Healed()
                    self.setKnownState("R")
                elif state == "D" :
                    self.__real = self.Died()
                    self.setKnownState("D")
                elif state == "V" :
                    self.__real = self.Vacinated()
                    self.setKnownState("V")

        def getKnownState(self) :
            return self.__known

        def setKnownState(self, state) :
            state = DataInfection().checkState(state)
            if state != None :
                self.__known = state

        def __assignDurationIncubation(self) :
            gauss = self.getInfection().getGaussIncubation()
            return Stats.partInt(Stats.getFoldedNormal(gauss[0], gauss[1]))

        def __assignInfectiousState(self) :
            infection = self.getInfection()
            gauss = self.getInfection().getGaussScore()
            score = Stats.getFoldedNormal(gauss[0], gauss[1])
            if score <= infection.getInfThreshold() :
                state = "A"
            elif score <= infection.getSupThreshold() :
                state = "I-"
            elif score <= infection.getDeathThreshold() :
                state = "I+"
            else :
                state = "D"
            return state, Stats.partInt(score)

        def dayUpdate(self, infectious_update) :
            update = self.getState().dayUpdate(infectious_update)
            state = update.get("state")
            if state != None :
                if state == "I" :
                    state, score = self.__assignInfectiousState()
                    self.setState(state, score)
                else :
                    self.setState(state)

        class Susceptible () :
            def __init__(self, days_accumulation, infection_threshold) :
                self.__length = days_accumulation
                self.__infection_threshold = infection_threshold
                self.__particles = list()

            def getName(self) :
                return "S"

            def getParticles(self) :
                return self.__particles

            def getThreshold(self) :
                return self.__infection_threshold

            def __addParticle(self, particle) :
                self.__particles.append(particle)
                if len(self.__particles) > self.__length :
                    del(self.__particles[0])

            def __sumParticles(self) :
                sum = 0
                for day in self.__particles :
                    sum += day
                return sum

            def dayUpdate(self, infectious_update) :
                particle = infectious_update.get("particle",0)
                self.__addParticle(particle)
                if self.__sumParticles() > self.getThreshold() :
                    return {"state" : "E"}
                else :
                    return {"state" : None}

        class Incubation () :
            def __init__(self, duration, emission) :
                self.__duration = duration
                self.__emission = emission

            def getName(self) :
                return "E"

            def getDuration(self) :
                return self.__duration

            def getEmission(self) :
                return self.__emission

            def __decreaseDuration(self) :
                self.__duration -= 1

            def dayUpdate(self, infectious_update) :
                self.__decreaseDuration()
                if self.getDuration() <= 0 :
                    return {"state" : "I"}
                else :
                    return {"state" : None}

        class Asymptomatic () :
            def __init__(self, score, emission, healing) :
                self.__score = score
                self.__emission = emission
                self.__healing = healing

            def getName(self) :
                return "A"

            def getScore(self) :
                return self.__score

            def getEmission(self) :
                return self.__emission

            def getHealing(self) :
                return self.__healing

            def __applyHealing(self) :
                self.__score -= self.__healing

            def dayUpdate(self, infectious_update) :
                self.__applyHealing()
                if self.getScore() <= 0 :
                    return {"state" : "R"}
                else :
                    return {"state" : None}

        class Standard () :
            def __init__(self, score, emission, healing, serious_threshold) :
                self.__score = score
                self.__emission = emission
                self.__healing = healing
                self.__serious_threshold = serious_threshold

            def getName(self) :
                return "I-"

            def getScore(self) :
                return self.__score

            def getEmission(self) :
                return self.__emission

            def getHealing(self) :
                return self.__healing

            def getSeriousThreshold(self) :
                return self.__serious_threshold

            def __applyHealing(self) :
                self.__score -= self.__healing

            def dayUpdate(self, infectious_update) :
                self.__applyHealing()
                if self.getScore() <= 0 :
                    return {"state" : "R"}
                elif self.getScore() >= self.getSeriousThreshold() :
                    return {"state" : "I+", "score" : self.getScore()}
                else :
                    return {"state" : None}

        class Serious () :
            def __init__(self, score, emission, aggravation, death_threshold) :
                self.__score = score
                self.__emission = emission
                self.__aggravation = aggravation
                self.__death_threshold = death_threshold

            def getName(self) :
                return "I+"

            def getScore(self) :
                return self.__score

            def getEmission(self) :
                return self.__emission

            def getAggravation(self) :
                return self.__aggravation

            def getDeathThreshold(self) :
                return self.__death_threshold

            def __applyAggravation(self) :
                self.__score += self.__aggravation

            def dayUpdate(self, infectious_update) :
                self.__applyAggravation()
                if self.getScore() <= 0 :
                    return {"state" : "R"}
                elif self.getScore() >= self.getDeathThreshold() :
                    return {"state" : "D"}
                else :
                    return {"state" : None}

        class Healed () :
            def __init__(self) :
                pass

            def getName(self) :
                return "R"

            def dayUpdate(self, infectious_update) :
                return {"state" : None}

        class Died () :
            def __init__(self) :
                pass

            def getName(self) :
                return "D"

            def dayUpdate(self, infectious_update) :
                return {"state" : None}

        class Vacinated () :
            def __init__(self) :
                pass

            def getName(self) :
                return "V"

            def dayUpdate(self, infectious_update) :
                return {"state" : None}
'''