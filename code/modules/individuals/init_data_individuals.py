from modules.individuals.data_individuals import DataIndividuals, Individual
from modules.places.init_data_places import all_place_typages
from modules.tools.style import Color
from tqdm import tqdm
import numpy as np
from random import randint


individual_count = {
    'type_set' : 'rate',
    'values' : {
        'child' : 0.05,
        'kid' : 0.15,
        'worker' : 0.45,
        'non_worker' : 0.05,
        'retired' : 0.28,
        'prisoner' : 0.02
        },
    'total_number' : 500
    }

individual_typages = {
    'child' : {
        'factor' : 1,
        'age_min' : 0,
        'age_max' : 4,
        'home' : ("accomodation", "housing"),
        'work' : 'home'
        },
    'kid' : {
        'factor' : 1,
        'age_min' : 5,
        'age_max' : 19,
        'home' : ("accomodation", "housing"),
        'work' : [("education", "school"), ("education", "academic"),
                  ("education", "others")]
        },
    'worker' : {
        'factor' : 1,
        'age_min' : 20,
        'age_max' : 65,
        'home' : ("accomodation", "housing"),
        'work' : all_place_typages
        },
    'non_worker' : {
        'factor' : 1,
        'age_min' : 20,
        'age_max' : 65,
        'home' : ("accomodation", "housing"),
        'work' : 'home'
        },
    'retired' : {
        'factor' : 1,
        'age_min' : 66,
        'age_max' : 95,
        'home' : [("accomodation", "housing"), ("accomodation", "pension")],
        'work' : 'home'
        },
    'prisoner' : {
        'factor' : 1,
        'rate' : 0.02,
        'age_min' : 18,
        'age_max' : 80,
        'home' : ("accomodation", "prison"),
        'work' : 'home'
        }
    }


def init_individuals_database(dataindividuals) :
    print(f"{Color.CYAN}Set individuals from predefined instructions in progress ..."
           f"{Color.RESET}")
    if individual_count['type_set'] == 'rate' :
        total_number = individual_count['total_number']
        with tqdm(total=total_number, desc=f"Inserting individuals") as pbar:
            for type_name in individual_count['values'].keys():
                for i in np.arange(int(total_number*individual_count['values'][type_name])):
                    age_min = individual_typages[type_name]['age_min']
                    age_max = individual_typages[type_name]['age_max']
                    random_age = randint(age_min, age_max)
                    dataindividuals.insert_individual(type_name, type_name, random_age)
                    pbar.update(1)
    elif individual_count['type_set'] == 'number' :
        pass
    else :
        raise ValueError(f"{Color.GREEN}type_set{Color.RESET} argument is not"
                         "recognized. Must be among ('rate', 'number').\n")


