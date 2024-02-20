from modules.tools.style import Color
from modules.scripts.data_scripts import Script, Trip
from modules.places.data_places import Place
from modules.places.data_occupancy_places import OccupancyPlace, SubOccupancy
from collections import defaultdict
from tqdm import tqdm


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
                    print(f"{Color.RED}Warning :{Color.RESET} Script related to "
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
                           f' to="{destination_place_road_id}" modes="{transport}" />')
                file.write('\n\t\t</person>')
                trip+=1

    def update_individuals_trips_duration(self, tripinfo_file, day):
        print(f"{Color.CYAN}Update individual trips duration with digitalized results "
              f"for day {day} in progress ...{Color.RESET}")
        duration_trips = defaultdict(dict)
        reader = open(f'{tripinfo_file}', 'r')
        buffer = reader.readline().split()
        while len(buffer)>0:
            if buffer[0]=='<personinfo':
                individual_id, trip = self.__get_tag_from_tripinfo_split_buffer(buffer, 'id').split('#')
                buffer = reader.readline().split()
                transport_duration = self.__get_tag_from_tripinfo_split_buffer(buffer, 'duration')
                duration_trips[individual_id][trip] = transport_duration
            buffer = reader.readline().split()
        if len(list(duration_trips.keys()))>1:
            with tqdm(total=len(list(duration_trips.keys())), desc="Updating real duration trips") as pbar:
                for individual_id in list(duration_trips.keys()):
                    self.__update_individual_trip_duration_(day, individual_id, duration_trips[individual_id])
                    pbar.update(1)

    def __update_individual_trip_duration(self, day, individual_id, trips_duration_dict):
        script = self.datascripts.get_individual_day_script(day, individual_id)
        sequence = Script(script)['sequence'].copy.deepcopy()
        place_trips_index_not_visited = list()
        for trip in range(len(trips_duration_dict.keys())):
            time_after_transport = Trip(sequence[trip])['end_time']+trips_duration_dict[trip]
            sequence[trip+1][1] = int(time_after_transport)
            # raise warning if start_time is higher than end_time and delete trip
            duration = Trip(sequence[trip])['end_time'] - Trip(sequence[trip])['start_time']
            if duration < 0 :
                print(f"{Color.RED}Warning :{Color.RESET} Individual id {individual_id} "
                      f"has not really visited place id {{sequence[trip+1][0]}} "
                      f"during the day {day}.")
                time_added_for_transport_to_unvisited_place = duration*-1
                place_trips_index_not_visited.append([trip+1, time_added_for_transport_to_unvisited_place])
        for error_trip in reversed(place_trips_index_not_visited):
            trip_index, added_time = error_trip
            sequence[trip_index+1][1] += added_time
            del sequence[trip_index]
            # support consecutive not visited places
        self.datascripts.assign_sequence_to_individual_day_script(day, individual_id, sequence)
        self.datascripts.assign_bool_computed_trips_duration_to_individual_day_script(day, individual_id, 1)


    def __get_tag_from_tripinfo_split_buffer(self, split_buffer, tag):
        list_ = list()
        for token in split_buffer :
            list_.extend(token.split('"'))
        tag = f'{tag}='
        if tag in list_ :
            return list_[list_.index(tag)+1]
        else :
            return None


    def update_occupancy_places(self, day, dataoccupancyplaces):
        print(f"{Color.CYAN}Update observed occupancy places with digitalized results "
              f"for day {day} in progress ...{Color.RESET}")
        all_scripts = self.datascripts.get_day_scripts(day)
        with tqdm(total=len(all_scripts), desc="Updating occupancy places") as pbar:
            for script in all_scripts:
                individual_id = Script(script)["individual_id"]
                sequence = Script(script)["sequence"]
                for trip in sequence:
                    place_id = Trip(trip)['place_id']
                    start_time = Trip(trip)['start_time']
                    end_time = Trip(trip)['end_time']
                    occupancy_places = dataoccupancyplaces.get_day_occupancy_place(day, place_id)
                    if len(occupancy_places)>0 :
                        occupancy = OccupancyPlace(occupancy_places)['occupancy']
                    else:
                        occupancy = occupancy_places
                    occupancy.append([start_time, end_time, individual_id])
                    dataoccupancyplaces.assign_day_occupancy_to_place(day, place_id, str(occupancy))
        # sort occupancy according to start_time
        for place_id in self.dataplaces.list_all_ids() :
            occupancy_places = dataoccupancyplaces.get_day_occupancy_place(day, place_id)
            occupancy = OccupancyPlace(occupancy_places)['occupancy']
            occupancy = sorted(occupancy, key=lambda x:x[0])
            dataoccupancyplaces.assign_day_occupancy_to_place(day, place_id, str(occupancy))
