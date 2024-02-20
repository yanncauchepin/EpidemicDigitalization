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
from modules.places.data_occupancy_places import DataOccupancyPlaces, OccupancyPlace
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

def set_infections_and_individual_infections(datainfections, dataindividuals,
                                             dataindividualinfections):
    datainfections.create_database()
    datainfections.reset_database()
    init_infections_database(datainfections)
    dataindividualinfections.create_database()
    dataindividualinfections.reset_database()
    init_individual_infections_database(datainfections, dataindividuals, dataindividualinfections)



if __name__ == '__main__' :

    # input paths
    root_path = os.getcwd()
    osm_dataset_path = '../datasets/belval/openstreetmap/belval.osm.xml'
    places_database_path = 'databases/data_places.db'
    roads_database_path = 'databases/data_roads.db'
    individuals_database_path = 'databases/data_individuals.db'
    infections_database_path = 'databases/data_infections.db'
    individual_infections_database_path = 'databases/data_individual_infections.db'
    scripts_database_path = 'databases/data_scripts.db'
    occupancy_places_database_path = 'databases/data_occupancy_places.db'
    

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
    dataoccupancyplaces = DataOccupancyPlaces(occupancy_places_database_path, dataplaces) 
    dataoccupancyplaces.create_database()
    dataoccupancyplaces.reset_database()

    # init digitalization and handlers
    day_max = 2
    day=0
    scriptshandler = ScriptsHandler(dataplaces, dataindividuals, datascripts)
    infectionshandler = InfectionsHandler(datainfections, dataindividualinfections,
                                          dataplaces, dataoccupancyplaces, datascripts)

    # run digitalization
    while day < day_max:
        # configure day
        init_scripts_database(dataplaces, dataindividuals, datascripts, day)
        sumohandler.init_day_individuals_routes(scriptshandler, day)
        sumohandler.init_day_config_sumomobility(day)
        sumohandler.run_day(day, verbose=False)
        # get and update output
        output_trips_file = sumohandler.get_day_output_trips_file(day)
        scriptshandler.update_individuals_trips_duration(output_trips_file, day)
        scriptshandler.update_occupancy_places(day, dataoccupancyplaces)
        infectionshandler.update_individual_infections()
        '''
        dataindividualinfections.count_by_infection_real_state()
        dataindividualinfections.count_by_infection_known_state()
        '''
        day+=1
