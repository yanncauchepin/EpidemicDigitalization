from modules.tools.style import Color
from tqdm import tqdm

infections = {
    "covid19" : {
        }
    }

def init_infections_database(datainfections):
    print(f"{Color.CYAN}Set infections from predefined instructions in progress ..."
           f"{Color.RESET}")
    all_infections = infections.keys()
    with tqdm(total=len(all_infections), desc=f"Inserting infections") as pbar:
        for infection in all_infections :
            datainfections.insert_infection(infection, **infections[infection])
            pbar.update(1)

def init_individual_infections_database(datainfections, dataindividuals, dataindividualinfections):
    print(f"{Color.CYAN}Set individual infections from predefined instructions"
          f" in progress ...{Color.RESET}")
    all_infections = datainfections.list_all_names()
    all_individuals = dataindividuals.list_all_ids()
    with tqdm(total=len(all_infections)*len(all_individuals), 
              desc=f"Inserting individual infections") as pbar:
        for infection_name in all_infections:
            for individual_id in all_individuals:
                dataindividualinfections.insert_individual_infection(infection_name, individual_id)
                pbar.update(1)

'''----------------------------------------------------------------> DEPRECATED

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
'''