from Modules.Infection import DataInfection
from Modules.Person import DataPerson
from Modules.Tools.Style import color
from Modules.Tools import Stats
from random import sample

def initCovidDataInfection(proba, min_person=None):

    datainfection = DataInfection.DataInfection()
    datainfection.addInfection("Covid")
    initPeopleInfection("Covid", proba, min_person)
    return datainfection

def initPeopleInfection(infection, proba, min_person=None):

    dataperson = DataPerson.DataPerson()
    people = dataperson.getPeople()
    datainfection = DataInfection.DataInfection()
    infection = datainfection.getInfection(infection)
    if infection != None :
        infection = infection.getName()
        number = Stats.partInt(len(people)*proba)
        if min_person != None and number < min_person :
            number = Stats.partInt(min_person)
        if number < 1 :
            print(f"{color.RED}Error :{color.RESET} No person has been infected")
        r = sample(people, number)
        for infected in r :
            datainfection.addPersonState(infection, infected, initial_state="E")
            people.remove(infected)
        for healthy in people :
            datainfection.addPersonState(infection, healthy, initial_state="S")
