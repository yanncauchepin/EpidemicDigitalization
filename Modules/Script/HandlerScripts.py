from Modules.Person import DataPerson
from Modules.Script import DataScript
from Modules.Place import DataPlace
from Modules.Tools.Style import color

FULL_TRANSPORT = ["public", "car", "bicycle", "taxi"]

def __assignFullTransport() :
    return "public car bicycle taxi"

def __validTransport(original) :
    transport = ""
    for elem in original :
        if elem in FULL_TRANSPORT :
            transport += f"{str(elem)} "
    if transport == "" :
        return None
    else :
        return transport

def initPeopleTrips(file, day):

    file = open(file, "w")
    file.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">')
    dataperson = DataPerson.DataPerson()
    for person in dataperson.getPeople() :
        person = dataperson.getPerson(person)
        transport = "public"
        #transport = person.getFeature("transport")
        #transport = __validTransport(transport)
        #if transport == None :
        #    transport = __assignFullTransport()
            #transport = "public"
        script = person.getDayScript(day)
        if script == None :
            print(f"{color.RED}Error : {color.RESET}Person {color.BLUE}{person.getId()}{color.RESET} has no script for day {color.CYAN}{day}{color.RESET}")
        else :
            setTripPerson(file, person.getId(), day, script, transport)
    file.write('\n</routes>')
    file.close()

def setTripPerson(file, person, day, script, transport) :

    sequence = DataScript.DataScript().getScript(script).getSequence()
    if len(sequence)>2 :
        dataplace = DataPlace.DataPlace()
        length = len(sequence)-1
        trip = 0
        while trip < length :
            file.write(f'\n\t\t<person id="{person}#{trip}" depart="{sequence[trip][2]}" >')
            file.write(f'\n\t\t\t\t<personTrip from="{dataplace.getPlace(sequence[trip][0]).getRoad()}" to="{dataplace.getPlace(sequence[trip+1][0]).getRoad()}" modes="{transport}" />')
            file.write('\n\t\t</person>')
            trip+=1

def getPeopleTripsDuration(day) :

    trips = dict()
    dataperson = DataPerson.DataPerson()
    for person in dataperson.getPeople() :
        trips[person] = list()
    file = f"Modules/SumoMobility/Report/{day}.tripinfo.xml"
    reader = open (f"{file}", "r")
    buffer = reader.readline()
    while buffer != '' :
        buffer = buffer.split()
        if len(buffer) > 0 :
            if buffer[0] == "<personinfo" :
                person, trip = getTagFromBuffer(buffer, "id").split("#")
                buffer = reader.readline().split()
                transport_duration = getTagFromBuffer(buffer, "duration")
                trips[int(person)].append([int(trip), float(transport_duration)])
                print(f"{person} : trip n°{trip}, {transport_duration} seconds")
        buffer = reader.readline()
    return trips

def getTagFromBuffer(buffer, tag) :

    extend_buffer = list()
    for elem in buffer :
        extend_buffer.extend(elem.split('"'))
    tag = tag + "="
    if tag in extend_buffer :
        return extend_buffer[extend_buffer.index(tag)+1]
    else :
        return None

def getPeopleTimePlace(day) :

    dataperson = DataPerson.DataPerson()
    datascript = DataScript.DataScript()
    people_transport = getPeopleTripsDuration(day)
    person_occupation = dict()
    for person in dataperson.getPeople() :
        transport = people_transport.get(person)
        sequence = datascript.getScript(dataperson.getPerson(person).getDayScript(day)).getSequence()
        for trip in range(len(transport)) :
            time = sequence[trip][2] + transport[trip][1]
            sequence[trip+1][1] = int(time)
            if sequence[trip+1][1] > sequence[trip+1][2] :
                sequence[trip+1].append("Error")
                print(f"{color.RED}Error :{color.RESET} Person {color.BLUE}{person}{color.RESET} does not occupy place {color.CYAN}{sequence[trip+1][0]}{color.RESET} (trip n°{trip}) during day {color.CYAN}{day}{color.RESET}")
        person_occupation[person] = sequence
    return person_occupation

def getPlaceOccupation(day) :

    dataplace = DataPlace.DataPlace()
    place_occupation = dict()
    for place in dataplace.getPlaces() :
        place_occupation[place] = list()
    dataperson = DataPerson.DataPerson()
    datascript = DataScript.DataScript()
    for person in dataperson.getPeople() :
        sequence = datascript.getScript(dataperson.getPerson(person).getDayScript(day)).getSequence()
        for place in sequence :
            if not place[-1] == "Error" :
                place_occupation[place[0]].append([place[1], place[2], person])
    for place in place_occupation.keys() :
        place_occupation[place].sort()
    return place_occupation
