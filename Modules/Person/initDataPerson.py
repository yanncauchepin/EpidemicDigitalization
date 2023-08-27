from Modules.Person import DataPerson, setPerson
from Modules.Place import DataPlace
from Modules.Data import Luxembourg
from Modules.Tools.Style import color
from math import floor
import random

def initPersonDataPerson (region=None, number=None) :

    demographic = Luxembourg.Demographic ()
    if number == None and region != None :
            number = demographic.getPopulationRegion(region)
    if number == None :
        print(f"{color.RED}Error :{color.RESET} Number of people not define")
    else :
        setPerson.setTypePeople("child", floor(number*0.2))
        setPerson.setTypePeople("worker", floor(number*0.5))
        setPerson.setTypePeople("non-worker", floor(number*0.1))
        setPerson.setTypePeople("retired", floor(number*0.15))
        setPerson.setTypePeople("prisoners", floor(number*0.05))

def assignTransportPeople() :

    dataperson = DataPerson.DataPerson()
    for person in dataperson.getPeople() :
        person = dataperson.getPerson(person)
        if person.getAge() <= 4 :
            person.addFeature("transport", ["public", "car"], change=True)
        elif person.getAge() <= 19 :
            r = random.random()
            if r <= 0.7 :
                person.addFeature("transport", ["public"], change=True)
            else :
                person.addFeature("transport", ["public", "bicycle"], change=True)
        elif person.getAge() <= 65 :
            r = random.random()
            if r <= 0.6 :
                person.addFeature("transport", ["public", "car"], change=True)
            elif r <= 0.8 :
                person.addFeature("transport", ["public", "bicycle"], change=True)
            else :
                person.addFeature("transport", ["public", "car", "bicycle", "taxi"], change=True)
        else :
            r = random.random()
            if r <= 0.3 :
                person.addFeature("transport", ["public", "car", "bicycle", "taxi"], change=True)
            else :
                person.addFeature("transport", ["public", "taxi"], change=True)

def assignHousingPerson() :

    dataperson = DataPerson.DataPerson()
    dataplace = DataPlace.DataPlace()

    accomodation_type = dataplace.getType("accomodation")
    accomodation_subtypes = accomodation_type.getSubtypes()
    for subtype in accomodation_subtypes :
        for place in accomodation_type.getSubtype(subtype).getPlaces() :
            dataplace.getPlace(place).addFeature("resident", list(), change=True)
    for type in dataperson.getTypes() :
        for subtype in dataperson.getType(type).getSubtypes() :
            accomodation = dataperson.getType(type).getSubtype(subtype).getFeature("accomodation")
            if accomodation == None :
                accomodation = accomodation_subtypes
            #check accomodation
            people = dataperson.getType(type).getSubtype(subtype).getPeople()
            places = list()
            cumul_area = 0
            for subtype in accomodation :
                for place in accomodation_type.getSubtype(subtype).getPlaces() :
                    cumul_area += dataplace.getPlace(place).getArea()
                    places.append([cumul_area, place])
            for person in people :
                if len(places)>0 :
                    r = random.randint(0,cumul_area)
                    place = 0
                    while r > places[place][0] and place < len(places) :
                        place += 1
                    place = places[place][1]
                    dataperson.getPerson(person).addFeature("home", place, change=True)
                    current = dataplace.getPlace(place).getFeature("resident")
                    new = list()
                    new.extend(current+[person])
                    dataplace.getPlace(place).addFeature("resident", new, change=True)
                else :
                    dataperson.getPerson(person).addFeature("home", None, change=True)

def initTypageDataPerson ():

    dataperson = DataPerson.DataPerson()

    dataperson.addTypePerson("child")
    type = dataperson.getType("child")
    type.addSubtypePerson("baby")
    subtype = type.getSubtype("baby")
    subtype.addFeature("age_min", 0)
    subtype.addFeature("age_max", 4)
    subtype.addFeature("accomodation", ["housing"])
    type.addSubtypePerson("kid")
    subtype = type.getSubtype("kid")
    subtype.addFeature("age_min", 5)
    subtype.addFeature("age_max", 19)
    subtype.addFeature("accomodation", ["housing"])

    dataperson.addTypePerson("worker")
    type = dataperson.getType("worker")
    type.addSubtypePerson("worker")
    subtype = type.getSubtype("worker")
    subtype.addFeature("age_min", 20)
    subtype.addFeature("age_max", 65)
    subtype.addFeature("accomodation", ["housing"])

    dataperson.addTypePerson("non-worker")
    type = dataperson.getType("non-worker")
    type.addSubtypePerson("non-worker")
    subtype = type.getSubtype("non-worker")
    subtype.addFeature("age_min", 20)
    subtype.addFeature("age_max", 65)
    subtype.addFeature("accomodation", ["housing"])

    dataperson.addTypePerson("retired")
    type = dataperson.getType("retired")
    type.addSubtypePerson("retired")
    subtype = type.getSubtype("retired")
    subtype.addFeature("age_min", 66)
    subtype.addFeature("age_max", 95)
    subtype.addFeature("accomodation", ["pension", "housing"])

    dataperson.addTypePerson("prisoners")
    type = dataperson.getType("prisoners")
    type.addSubtypePerson("prisoners")
    subtype = type.getSubtype("prisoners")
    subtype.addFeature("age_min", 19)
    subtype.addFeature("age_max", 80)
    subtype.addFeature("accomodation", ["prison"])

    return dataperson
