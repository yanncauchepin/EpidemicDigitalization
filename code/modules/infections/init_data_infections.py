from modules.tools.style import Color
from tqdm import tqdm

infections = {
    "covid19" : {
        }
    }

def init_infections_database(datainfections):
    print(f"{Color.CYAN}Set infections from predefined instructions in progress ..."
           f"{Color.RESET}")
    all_infections = infections.keys()
    with tqdm(total=len(all_infections), desc=f"Inserting infections") as pbar:
        for infection in all_infections :
            datainfections.insert_infection(infection, **infections[infection])
            pbar.update(1)

def init_individual_infections_database(datainfections, dataindividuals, dataindividualinfections):
    print(f"{Color.CYAN}Set individual infections from predefined instructions"
          f" in progress ...{Color.RESET}")
    all_infections = datainfections.list_all_names()
    all_individuals = dataindividuals.list_all_ids()
    with tqdm(total=len(all_infections)*len(all_individuals),
              desc=f"Inserting individual infections") as pbar:
        for infection_name in all_infections:
            for individual_id in all_individuals:
                dataindividualinfections.insert_individual_infection(infection_name, individual_id)
                pbar.update(1)
