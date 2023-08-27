from Modules.Person import DataPerson
from Modules.Infection import DataInfection
from Modules.Place import DataPlace
from Modules.Script import DataScript
from Modules.Tools import Stats
from Modules.Tools.Style import color

datainfection = DataInfection.DataInfection()
dataperson = DataPerson.DataPerson()
dataplace = DataPlace.DataPlace()
datascript = DataScript.DataScript()

def assessPeopleInfection(day, infection, occupency_place) :

    infection = datainfection.getInfection(infection)
    if infection != None :
        infection = infection.getName()
        people = dataperson.getPeople()
        for person in people :
            #print("getPersonInfectionUpdate")
            infectious_update = getPersonInfectiousUpdate(day, infection, person, occupency_place)
            #print("dayUpdate")
            datainfection.getPersonState(infection, person).dayUpdate(infectious_update)

def getPersonInfectiousUpdate(day, infection, person, occupency_place) :

    #print(f"Person {person}")
    person_state = datainfection.getPersonState(infection, person)
    infectious_update = None
    if person_state != None :
        state = person_state.getRealState()
        #print(f"State {state}")
        if state == "S" :
            infectious_update = getPersonSusceptibleUpdate(day, infection, person, occupency_place)
    return infectious_update

def getPersonSusceptibleUpdate(day, infection, person, occupency_place) :

    script = dataperson.getPerson(person).getDayScript(f"default.{day}")
    sequence = datascript.getScript(script).getSequence()
    particle = 0
    for visit in sequence :
        if visit[-1] != "Error" :
            place_particle = getParticlePlaceInTime(infection, visit[0], occupency_place[visit[0]], visit[1])
            people_particle = getParticlePersonDuringTime(infection, visit[0], occupency_place[visit[0]], visit[1], visit[2])
            particle += Stats.partInt(place_particle*0.1) + people_particle
    return {"particle" : particle}

def getParticlePlaceInTime(infection, place, occupency, start) :

    place = dataplace.getPlace(place)
    infection = datainfection.getInfection(infection)
    if place != None and infection != None :
        duration = infection.getSecondsCumulPlace()
        infection = infection.getName()
        length = len(occupency) - 1
        visit = 0
        particles = 0
        #print("PARTICLEPLACE")
        #print(occupency)
        #print(start)
        while occupency[visit][0] < start and visit < length :
            if start - occupency[visit][0] <= duration :
                state = datainfection.getPersonState(infection, occupency[visit][2]).getState()
                if state.getName() in ("E", "A", "I-", "I+") :
                    if occupency[visit][1] > start :
                        last = start - occupency[visit][0]
                    else :
                        last = occupency[visit][1] - occupency[visit][0]
            visit += 1
        #print(occupency[visit])
    return particles

def getParticlePersonDuringTime(infection, place, occupency, start, end) :

    place = dataplace.getPlace(place)
    infection = datainfection.getInfection(infection)
    if place != None and infection != None :
        infection = infection.getName()
        length = len(occupency) - 1
        visit = 0
        particles = 0
        #print("PARTICLEPERSON")
        #print(occupency)
        #print(start)
        #print(end)
        while occupency[visit][0] <= end and visit < length :
            if occupency[visit][1] > start :
                state = datainfection.getPersonState(infection, occupency[visit][2]).getState()
                if state.getName() in ("E", "A", "I-", "I+") :
                    if occupency[visit][0] < start :
                        first = start
                    else :
                        first = occupency[visit][0]
                    if occupency[visit][1] > end :
                        last = end
                    else :
                        last = occupency[visit][1]
                    particles += (last - first) * state.getEmission()
            visit += 1
        #print(occupency[visit])
    return particles
