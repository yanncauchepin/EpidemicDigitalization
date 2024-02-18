from modules.infections.data_infections import Infection
from modules.infections.data_individual_infections import IndividualInfection
from modules.scripts.data_scripts import Script, Trip
from modules.places.data_occupancy_places import OccupancyPlace, SubOccupancy
from modules.tools.style import Color
from tqdm import tqdm
import random

class InfectionsHandler():
    
    def __init__(self, datainfections, dataindividualinfections, dataplaces, 
                 dataoccupancyplaces, datascripts):
        self.datainfections = datainfections
        self.dataindividualinfections = dataindividualinfections
        self.dataplaces = dataplaces
        self.dataoccupancyplaces = dataoccupancyplaces
        self.datascripts = datascripts
        
    def update_individual_infections(self, day, dataplaces):
        print(f"{Color.CYAN}Updating individual infections with digitalized results "
              f"in progress ...{Color.RESET}")
        all_infections = self.datainfections.list_all_names()
        with tqdm(total=len(all_infections), desc="Updating infections") as pbar_infections:
            for infection_name in all_infections:
                all_individuals = self.dataindividualinfections.list_all_individuals_by_infection(infection_name)
                with tqdm(total=len(all_individuals), desc=f"Updating {infection_name}") as pbar_individuals:
                    for individual_id in all_individuals :
                        self.__update_indivual_infection(day, infection_name, individual_id)
                        pbar_individuals.update(1)
                pbar_infections.update(1)
                        
    
    def __update_indivual_infection(self, day, infection_name, individual_id):
        individual_infection = self.dataindividualinfections.get_individual_infection(infection_name, individual_id)
        real_state = IndividualInfection(individual_infection)['real_state']
        match real_state:
            case 'S':
                 self.__update_susceptible_individual_infection(day, infection_name, individual_id)
            case 'E':
                 individual_infection = self.dataindividualinfections.get_individual_infection(infection_name, individual_id)
                 incubation_duration = IndividualInfection(individual_infection)['incubation_duration']
                 incubation_duration -= 1
                 self.dataindividualinfections.assign_incubation_duration_to_individual_infection(
                     infection_name, individual_id, incubation_duration)
                 if incubation_duration==0:
                     self.__init_infectious_individual_infection()
                     self.dataindividualinfections.assign_incubation_duration_to_individual_infection(
                         infection_name, individual_id, None)
                     
            case 'A', 'I-', 'I+':
                 infection = self.datainfections.get_infection(infection_name)
                 death_threshold = Infection(infection)["death_threshold"]
                 individual_infection = self.dataindividualinfections.get_individual_infection(infection_name, individual_id)
                 infection_score = IndividualInfection(individual_infection)['infection_score']
                 immune_reaction = IndividualInfection(individual_infection)['immune_reaction']
                 infection_score += immune_reaction
                 if infection_score<=0:
                     self.dataindividualinfections.assign_real_state_to_individual_infection(
                         infection_name, individual_id, 'R')
                     self.dataindividualinfections.assign_infection_score_to_individual_infection(
                         infection_name, individual_id, 0)
                     self.dataindividualinfections.assign_emission_to_individual_infection(
                         infection_name, individual_id, 0)
                     self.dataindividualinfections.assign_immune_reaction_to_individual_infection(
                         infection_name, individual_id, 0)
                     self.dataindividualinfections.assign_infection_end_to_individual_infection(
                         infection_name, individual_id, day)
                 elif infection_score>death_threshold:
                     self.dataindividualinfections.assign_real_state_to_individual_infection(
                         infection_name, individual_id, 'D')
                     self.dataindividualinfections.assign_known_state_to_individual_infection(
                         infection_name, individual_id, 'D')
                     self.dataindividualinfections.assign_infection_score_to_individual_infection(
                         infection_name, individual_id, 0)
                     self.dataindividualinfections.assign_emission_to_individual_infection(
                         infection_name, individual_id, 0)
                     self.dataindividualinfections.assign_immune_reaction_to_individual_infection(
                         infection_name, individual_id, 0)
                     self.dataindividualinfections.assign_infection_end_to_individual_infection(
                         infection_name, individual_id, day)
                 else:
                      self.dataindividualinfections.assign_infection_score_to_individual_infection(
                          infection_name, individual_id, infection_score)
                      
            case _ :
                 pass

    
    def __init_infectious_individual_infection(self, day, infection_name, individual_id):
        infection = self.datainfections.get_infection(infection_name)
        mean_gaussian_infection = Infection(infection)["mean_gaussian_infection"]
        std_gaussian_infection = Infection(infection)["std_gaussian_infection"]
        lower_threshold = Infection(infection)["lower_threshold"]
        upper_threshold = Infection(infection)["upper_threshold"]
        asymptomatic_emission = Infection(infection)["asymptomatic_emission"]
        standard_emission = Infection(infection)["standard_emission"]
        serious_emission = Infection(infection)["serious_emission"]
        asymptomatic_healing = Infection(infection)["asymptomatic_healing"]
        standard_healing = Infection(infection)["standard_healing"]
        serious_aggravation = Infection(infection)["serious_aggravation"]
        if serious_aggravation>0:
            serious_emission = serious_emission*-1
        self.dataindividualinfections.assign_infection_start_to_individual_infection(
            infection_name, individual_id, day)
        infection_score = random.gauss(mean_gaussian_infection, std_gaussian_infection)
        if infection_score<0:
            infection_score*-1
        if infection_score<lower_threshold :
            self.dataindividualinfections.assign_real_state_to_individual_infection(
                infection_name, individual_id, 'A')
            self.dataindividualinfections.assign_infection_score_to_individual_infection(
                infection_name, individual_id, infection_score)
            self.dataindividualinfections.assign_emission_to_individual_infection(
                infection_name, individual_id, asymptomatic_emission)
            self.dataindividualinfections.assign_immune_reaction_to_individual_infection(
                infection_name, individual_id, asymptomatic_healing)
        elif infection_score>lower_threshold and infection_score<upper_threshold:
            self.dataindividualinfections.assign_real_state_to_individual_infection(
                infection_name, individual_id, 'I-')
            self.dataindividualinfections.assign_infection_score_to_individual_infection(
                infection_name, individual_id, infection_score)
            self.dataindividualinfections.assign_emission_to_individual_infection(
                infection_name, individual_id, standard_emission)
            self.dataindividualinfections.assign_immune_reaction_to_individual_infection(
                infection_name, individual_id, standard_healing)
        elif infection_score>upper_threshold:
            self.dataindividualinfections.assign_real_state_to_individual_infection(
                infection_name, individual_id, 'I+')
            self.dataindividualinfections.assign_known_state_to_individual_infection(
                infection_name, individual_id, 'I+')
            self.dataindividualinfections.assign_infection_score_to_individual_infection(
                infection_name, individual_id, infection_score)
            self.dataindividualinfections.assign_emission_to_individual_infection(
                infection_name, individual_id, serious_emission)
            self.dataindividualinfections.assign_immune_reaction_to_individual_infection(
                infection_name, individual_id, serious_aggravation)
    
    def __update_susceptible_individual_infection(self, current_day, infection_name, individual_id):
        particles = 0
        infection = self.datainfections.get_infection(infection_name)
        individual_cumulative_days = Infection(infection)["individual_cumulative_days"]
        place_cumulative_minutes = Infection(infection)["place_cumulative_minutes"]
        contamination_threshold = Infection(infection)["contamination_threshold"]
        days = [current_day - i for i in range(individual_cumulative_days)]
        days = [day for day in days if day >=0]
        for day in days:
            particles += self.__compute_particles(day, infection_name, individual_id, place_cumulative_minutes)
        self.dataindividualinfections.assign_contamination_score_to_individual_infection(
            infection_name, individual_id, particles)
        if particles>contamination_threshold:
            self.__init_incubation_individual_infection(current_day, infection_name, individual_id)
            
    def __init_incubation_individual_infection(self, current_day, infection_name, individual_id):
        infection = self.datainfections.get_infection(infection_name)
        mean_gaussian_incubation = Infection(infection)["mean_gaussian_incubation"]
        std_gaussian_incubation = Infection(infection)["std_gaussian_incubation"]
        incubation_emission = Infection(infection)["incubation_emission"]
        duration = int(random.gauss(mean_gaussian_incubation, std_gaussian_incubation))
        self.dataindividualinfections.assign_incubation_duration_to_individual_infection(
            infection_name, individual_id, duration)
        self.dataindividualinfections.assign_contamination_score_to_individual_infection(
            infection_name, individual_id, 0)
        self.dataindividualinfections.assign_real_state_to_individual_infection(
            infection_name, individual_id, 'E')
        self.dataindividualinfections.assign_emission_to_individual_infection(
            infection_name, individual_id, incubation_emission)
    
    def __compute_sequence_particles(self, day, infection_name, individual_id, 
                                     place_cumulative_minutes):
        particles = 0
        sequence = Script(self.datascripts.get_individual_day_script(day, individual_id))['sequence']
        for trip in sequence:
            place_id, start_time, end_time = Trip(trip)['all'] # can bug due to non ordered dict
            proximity_particles = self.__compute_place_particles(day, infection_name, individual_id, 
                                                        place_id, start_time, end_time)
            start_cumulative_time = start_time-place_cumulative_minutes*60
            if start_cumulative_time<0:
                start_cumulative_time=0
            suspended_particles = self.__compute_place_particles(day, infection_name, individual_id, 
                                                        place_id, start_cumulative_time, start_time)
            particles += suspended_particles*0.1 + proximity_particles
        return particles
    
    def __compute_place_particles(self, day, infection_name, individual_id, place_id, 
                                  start_time, end_time, place_cumulative_minutes):
        occupancyplaces = self.dataoccupancyplaces.get_day_occupancy_place(day, place_id)
        custom_occupancy = OccupancyPlace(occupancyplaces)['occupancy'].copy.deepcopy()
        for visit in reversed(custom_occupancy):
            if SubOccupancy(visit)['individual_id'] == individual_id:
                custom_occupancy.remove(visit)
        particles = 0
        if start_time<0 :
            start_time=0
        visit = 0
        while SubOccupancy(custom_occupancy[visit])['start_time']<end_time:
            if SubOccupancy(custom_occupancy[visit])['end_time']>start_time:
                individual_infection = self.dataindividualinfections.get_individual_infection(infection_name, individual_id)
                real_state = IndividualInfection(individual_infection)['real_state']
                if real_state in self.datainfections.contaminated_states:
                    individual_emission = IndividualInfection(individual_infection)['emission']
                    temp_end_time = end_time
                    if SubOccupancy(custom_occupancy[visit])['end_time']<end_time:
                        temp_end_time = SubOccupancy(custom_occupancy[visit])['end_time']
                    temp_start_time = start_time
                    if SubOccupancy(custom_occupancy[visit])['start_time']>start_time:
                        temp_start_time = SubOccupancy(custom_occupancy[visit])['start_time']
                    particles += (temp_end_time-temp_start_time) * individual_emission
                    
            visit+=1
        return particles
            
            
            
        


'''----------------------------------------------------------------> DEPRECATED

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

'''