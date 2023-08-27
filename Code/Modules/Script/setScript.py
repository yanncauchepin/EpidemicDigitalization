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
