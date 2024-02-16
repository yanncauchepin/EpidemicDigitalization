from modules.place.data_place import DataPlace
from modules.place.osm_handler import OsmHandler


if __name__ == '__main__' :
    
    osm_path = 'dataset/openstreetmap/belval.osm.xml'
    places_dataset_path = 'dataset/databases/data_places.db'
    
    data_place = DataPlace(places_dataset_path)
    data_place.create_database()
    data_place.reset_database()
    OsmHandler().apply_file(osm_path)
    ''' Test
    data_place.insert_place(151161, "building", "hotel", 42.65454, 485.685, 48.6, "nan", "nan")
    places = data_place.get_all_places()
    for place in places :
        print(place)
    print(data_place.count_places())
    '''
    data_place.end_connection_db()
    




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