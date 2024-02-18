from modules.places.data_places import DataPlaces, Place
from modules.roads.data_roads import DataRoads, Road, assign_road_place
from modules.openstreetmap.osm_handler import OsmHandler
from modules.individuals.data_individuals import DataIndividuals, Individual
from modules.individuals.init_data_individuals import init_individuals_database
from modules.infections.data_infections import DataInfections, Infection
from modules.infections.data_individual_infections import DataIndividualInfections, IndividualInfection
from modules.infections.init_data_infections import init_infections_database, init_individual_infections_database
from modules.infections.infections_handler import InfectionsHandler
from modules.sumomobility.sumomobility_handler import SumomobilityHandler
from modules.scripts.data_scripts import DataScripts, Script
from modules.scripts.init_data_scripts import init_scripts_database
from modules.scripts.scripts_handler import ScriptsHandler
import os


def set_places_and_roads(dataplaces, dataroads, osm_dataset_path):
    dataplaces.create_database()
    dataplaces.reset_database()
    dataroads.create_database()
    dataroads.reset_database()
    OsmHandler(dataplaces, dataroads).apply_file(osm_dataset_path)
    print(f'~> {dataplaces.count_places()} Places')
    print(f'~> {dataroads.count_roads()} Roads')
    assign_road_place(dataplaces, dataroads)

def set_individuals(dataindividuals):
    dataindividuals.create_database()
    dataindividuals.reset_database()
    init_individuals_database(dataindividuals)
    print(f"~> {dataindividuals.count_individuals()} Individuals")

def set_infections_and_individual_infections(datainfections, dataindividuals,
                                             dataindividualinfections):
    datainfections.create_database()
    datainfections.reset_database()
    init_infections_database(datainfections)
    print(f"~> {datainfections.count_infections()} Infections")
    dataindividualinfections.create_database()
    dataindividualinfections.reset_database()
    init_individual_infections_database(datainfections, dataindividuals, dataindividualinfections)
    print(f"~> {dataindividualinfections.count_individual_infections()} Individual infections")


if __name__ == '__main__' :

    # input paths
    root_path = os.getcwd()
    osm_dataset_path = '../datasets/belval/openstreetmap/belval.osm.xml'
    places_database_path = 'modules/places/databases/data_places.db'
    roads_database_path = 'modules/roads/databases/data_roads.db'
    individuals_database_path = 'modules/individuals/databases/data_individuals.db'
    infections_database_path = 'modules/infections/databases/data_infections.db'
    individual_infections_database_path = 'modules/infections/databases/data_individual_infections.db'
    scripts_database_path = 'modules/scripts/databases/data_scripts.db'

    # init sumomobility
    sumohandler = SumomobilityHandler(root_path, osm_dataset_path)
    sumomobility_network_path = sumohandler.init_network()
    sumohandler.init_polygon()
    sumohandler.init_sumomobility_view()
    sumohandler.init_pt_routes()

    # init dataset
    dataplaces = DataPlaces(places_database_path)
    dataroads = DataRoads(roads_database_path, sumomobility_network_path)
    dataindividuals = DataIndividuals(individuals_database_path)
    datainfections = DataInfections(infections_database_path)
    dataindividualinfections = DataIndividualInfections(individual_infections_database_path,
                                                        dataindividuals, datainfections)
    set_places_and_roads(dataplaces, dataroads, osm_dataset_path)
    set_individuals(dataindividuals)
    set_infections_and_individual_infections(datainfections, dataindividuals,
                                             dataindividualinfections)
    datascripts = DataScripts(scripts_database_path, dataindividuals)
    datascripts.create_database()
    datascripts.reset_database()

    # init digitalization and handlers
    day_max = 2
    day=0
    scriptshandler = ScriptsHandler(dataplaces, dataindividuals, datascripts)
    infectionshandler = InfectionsHandler(datainfections, dataindividualinfections)

    # run digitalization
    while day < day_max:
        # configure day
        init_scripts_database(dataplaces, dataindividuals, datascripts, day)
        print(f"~> {datascripts.count_scripts_by_day(day)} Scripts for day {day}")
        sumohandler.init_day_individuals_routes(scriptshandler, day)
        sumohandler.init_day_config_sumomobility(day)
        sumohandler.run_day(day, verbose=False)
        # get and update output
        output_trips_file = sumohandler.get_output_trips_file()
        scriptshandler.update_individuals_trips_duration(output_trips_file, day)
        scriptshandler.update_occupancy_places(day)
        '''
        infectionshandler.update_individual_infections()
        dataindividualinfections.count_by_infection_real_state()
        dataindividualinfections.count_by_infection_known_state()
        '''
        day+=1



'''----------------------------------------------------------------> DEPRECATED

import os

from Modules.Place import initDataPlace
from Modules.Person import initDataPerson
from Modules.Script import initDataScript, HandlerScripts
from Modules.Infection import initDataInfection, assessInfection
from Modules.SumoMobility import HandlerSumo

LIMIT_DAY = 40

path = os.getcwd()
osm = "Modules/OSM/belval.osm.xml"

#   Initialize SumoMobility
handlersumo = HandlerSumo.HandlerSumo(path=path, osm=osm)
network = handlersumo.initNetwork()
handlersumo.initPolygon()
handlersumo.initSumoView()
handlersumo.setPtRoute()

#   Initialize DataPlace
dataplace = initDataPlace.initTypageDataPlace()
initDataPlace.initOsmElements(osm_file=f"{path}/{osm}", network_file=f"{path}/{network}")
initDataPlace.assignRoadPlace()

#   Initialize DataPerson
dataperson = initDataPerson.initTypageDataPerson()
initDataPerson.initPersonDataPerson(number=2000)
initDataPerson.assignTransportPeople()
initDataPerson.assignHousingPerson()

#   Initialize DataInfection
datainfection = initDataInfection.initCovidDataInfection(proba=1e-5, min_person=5)

#   Run simulation
day_person = dict()
day_place = dict()
division_state = dict()
for state in ["S", "E", "A", "I-", "I+", "D", "R", "V"] :
    division_state[state] = list()
day = 0
observation = 0
while day < LIMIT_DAY :
    initDataScript.initPeopleScript(people=dataperson.getPeople(), day=f"default.{day}", type="total_random")
    handlersumo.setDayPeopleRoute(day=f"default.{day}")
    handlersumo.initDaySumoConfig(day=f"default.{day}")
    handlersumo.runDay(day=f"default.{day}", show=True)
    day_person[day] = HandlerScripts.getPeopleTimePlace(day=f"default.{day}")
    day_place[day] = HandlerScripts.getPlaceOccupation(day=f"default.{day}")
    assessInfection.assessPeopleInfection(day, "Covid", day_place[day])
    day_division = datainfection.getInfection("Covid").getDivisionPersonState()
    for state in ["S", "E", "A", "I-", "I+", "D", "R", "V"] :
        division_state[state].append(day_division[state])
    day += 1


#   Plot Graphic
import numpy as np
import matplotlib.pyplot as plt

day = np.arange(40)
S = division_state["S"]
E = division_state["E"]
A = division_state["A"]
I = division_state["I-"]
II = division_state["I+"]
R = division_state["R"]
D = division_state["D"]
V = division_state["V"]
plt.clf()
plt.plot(day, S, ",-", color=[0.2,0.6,0.], linewidth=2, label="Susceptible")
plt.plot(day, E, ",-", color=[1.,0.6,0.], linewidth=2, label="Incubation")
plt.plot(day, A, ",-", color=[1.,0.,0.6], linewidth=2, label="Asymptomatic")
plt.plot(day, I, ",-", color=[1.,0.2,0.2], linewidth=2, label="Standard")
plt.plot(day, II, ",-", color=[0.5,0.,0.], linewidth=2, label="Serious")
plt.plot(day, R, ",-", color=[0.6,0.6,1.], linewidth=2, label="Healed")
plt.plot(day, D, ",-", color=[0.2,0.2,0.2], linewidth=2, label="Died")
plt.plot(day, V, ",-", color=[0.2,0.2,1.], linewidth=2, label="Vacinated")
plt.xlabel("Days")
plt.ylabel("People")
plt.grid()
plt.legend()
plt.show()

'''
