from modules.tools.style import Color
from modules.scripts.data_scripts import Script
from modules.places.data_places import Place
from collections import defaultdict


class ScriptsHandler():
    
    def __init__(self, dataplaces, dataindividuals, datascripts, 
                 raise_error_related_script_not_exists=False):
        self.dataplaces = dataplaces
        self.dataindividuals = dataindividuals
        self.datascripts = datascripts
        self.raise_error_related_script_not_exists = raise_error_related_script_not_exists

    def init_individuals_trips(self, file, day):
        file = open(file, "w")
        file.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">')
        for individual_id in self.dataindividuals.list_all_ids():
            transport = "public"
            script = self.datascripts.get_individual_day_script(day, individual_id)
            if script == None :
                if self.raise_error_related_script_not_exists :
                    raise ValueError (f"Script related to individual id {individual_id}"
                                      f"and day {day} does not exist in the scripts database.")
                else:
                    print(f"{color.RED}Warning :{color.RESET} Script related to "
                          f"individual id {individual_id} and day {day} does not "
                          "exist in the scripts database.")
            else :
                self.__init_individual_trip_from_script(file, individual_id, day,
                                                        script, transport)
        file.write('\n</routes>')
        file.close()
        
    def __init_individual_trip_from_script(self, file, individual_id, day, script, transport):
        sequence = Script(script)['sequence']
        if len(sequence)>2:
            length = len(sequence)-1
            trip=0
            while trip < length:
                file.write(f'\n\t\t<person id="{individual_id}#{trip}" depart="{sequence[trip][1]}" >')
                origin_place_road_id = Place(self.dataplaces.get_place(sequence[trip][0]))['road_id']
                destination_place_road_id = Place(self.dataplaces.get_place(sequence[trip+1][0]))['road_id'] 
                file.write(f'\n\t\t\t\t<personTrip from="{origin_place_road_id}"'
                           ' to="{destination_place_road_id}" modes="{transport}" />')
                file.write('\n\t\t</person>')
                trip+=1
                
    """"""
    
    def compute_individuals_time_places(self, day):
        pass
    
    def __compute_individuals_trips_duration(self, tripinfo_file, day):
        trips = defaultdict(list)
        reader = open(f'{tripinfo_file}', 'r')
        buffer = reader.readline().split()
        while len(buffer)>0:
            if buffer[0]=='<personinfo':
                individual_id, trip = self.__get_tag_from_tripinfo_split_buffer(buffer, 'id').split('#')
                buffer = reader.readline().split()
                transport_duration = self.__get_tag_from_tripinfo_split_buffer(buffer, 'duration')
                self.__compute_individual_trip_duration_(individual_id, trip, transport_duration)
            buffer = reader.readline().split()
                    
    '''
                 person, trip = getTagFromBuffer(buffer, "id").split("#")
                 buffer = reader.readline().split()
                 transport_duration = getTagFromBuffer(buffer, "duration")
                 trips[int(person)].append([int(trip), float(transport_duration)])
                 print(f"{person} : trip n°{trip}, {transport_duration} seconds")
         buffer = reader.readline()
     return trips
    '''
    
    def __compute_individual_trip_duration(self, individual_id, trip, duration):
        pass
                    
    def __get_tag_from_tripinfo_split_buffer(self, split_buffer, tag):
        list_ = list()
        for token in split_buffer :
            list_.extend(token.split('"'))
        tag = f'{tag}='
        if tag in list_ :
            return list_[list_.index(tag)+1]
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
    
    def getPeopleTripsDuration(file, day) :

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


'''----------------------------------------------------------------> DEPRECATED

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

'''
