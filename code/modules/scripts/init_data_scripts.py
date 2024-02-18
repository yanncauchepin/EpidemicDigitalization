from modules.individuals.data_individuals import DataIndividuals, Individual
from modules.tools.style import Color
import random
from tqdm import tqdm


class ScriptTypes() :
    
    def __init__(self, dataplaces, dataindividuals):
        self.dataplaces = dataplaces
        self.dataindividuals = dataindividuals
        self.time = 0
        self.lenght = 60000
        self.total_lenght = 86400
    
    def set_external_home_place_id(self) :
        return random.choice(self.dataplaces.list_ids_by_type('accomodation'))[0]
    

class TotalRandomScripts(ScriptTypes):
    
    def __init__(self, dataplaces, dataindividuals):
        super().__init__(dataplaces, dataindividuals)
    
    def init_individual_sequence(self, individual_id) :
        return self.__build_sequence(individual_id)
    
    def __set_random_time(self, lower, upper):
        return random.randint(lower, upper)
    
    def __set_random_next_place(self) :
        return random.choice(self.dataplaces.list_all_ids())
    
    def __build_sequence(self, individual_id) :
        sequence = list()
        individual = self.dataindividuals.get_individual(individual_id)
        home_id = Individual(individual)["home_place_id"]
        if home_id == None or home_id not in self.dataplaces.list_all_ids():
            home_id = self.set_external_home_place_id()
        self.time += self.__set_random_time(100,400)
        sequence.append([home_id, 0, self.time])
        while self.time < self.lenght:
            temp_time = self.time
            self.time += self.__set_random_time(720, 5600)
            next_place_id = self.__set_random_next_place()
            sequence.append([next_place_id, temp_time, self.time])
        sequence.append([home_id, self.time, self.total_lenght])
        return sequence
            
    
def init_scripts_database(dataplaces, dataindividuals, datascripts, day):
    print(f"{Color.CYAN}Generate scripts for day {day} from predefined instructions"
          f" in progress ...{Color.RESET}")
    all_individuals = dataindividuals.list_all_ids()
    total_random_scripts = TotalRandomScripts(dataplaces, dataindividuals)
    with tqdm(total=len(all_individuals), desc=f"Creating scripts for day {day}") as pbar:
        for individual_id in all_individuals:
            sequence = total_random_scripts.init_individual_sequence(individual_id)
            datascripts.insert_script(day, individual_id, "total_random", str(sequence), 0, "None")
            pbar.update(1)
    

'''----------------------------------------------------------------> DEPRECATED

from Modules.Person import DataPerson
from Modules.Script import DataScript, setScript
from Modules.Tools.Style import color

from Modules.Person import DataPerson
from Modules.Place import DataPlace
from Modules.Tools.Style import color
import random

SEQUENCE_LENGTH = 60000
SCRIPT_TYPES = ["total_random"]

def setExternalHome() :

    dataplace = DataPlace.DataPlace()
    r = random.choice(dataplace.getPlaces())
    return r

def TotalRandomSequence(person, day, **kwargs) :

    sequence = list()
    dataplace = DataPlace.DataPlace()
    places = dataplace.getPlaces()
    home = kwargs.get("home", person.getFeature("home"))
    if home == None or home not in dataplace.getPlaces() :
        home = setExternalHome()
    length = kwargs.get("lenght", SEQUENCE_LENGTH)
    time = random.randint(100,400)
    sequence.append([home, 0, time])
    last_time = time#
    while time < length :
        moment = random.randint(900,7200)
        time += moment
        place = random.choice(places)
        sequence.append([place, last_time, time])
        last_time = time#
    sequence.append([home, time, 86400])#
    return sequence

def selectTypeScript() :

    print(SCRIPT_TYPES)
    input("Select sequence type :", type)
    if not checkTypeScript(type) :
        type = None
    return type

def checkTypeScript(type) :

    if type in SCRIPT_TYPES :
        print(f"Sequence type {color.CYAN}{type}{color.RESET} recognized")
        return True
    else :
        print(f"{color.RED}Error :{color.RESET} Sequence type {color.CYAN}{type}{color.RESET} not recognized")
        return False

def applyTypeScript(sequence, person, day, **kwargs):

    person = DataPerson.DataPerson().getPerson(person)
    if sequence == "total_random" :
        return TotalRandomSequence(person, day)
    else :
        return None

def initPeopleScript(people, day, type=None, **kwargs):

    datascript = DataScript.DataScript()
    dataperson = DataPerson.DataPerson()

    if not setScript.checkTypeScript(type) :
        print(f"{color.RED}Error : {color.RESET}No sequence referenced" )
        type = DataScript.selectTypeScript()
    if setScript.checkTypeScript(type) :
        for person in people :
            if person in dataperson.getPeople() :
                datascript.addScript(person, day, type, **kwargs)
            else :
                print(f"{color.RED}Error :{color.RESET} Person {color.BLUE}{person}{color.RESET}not in dataperson")
'''