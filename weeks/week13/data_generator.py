import pendulum
import random 
import numpy as np

all_districts = [
        "Lisboa", "Porto", "Aveiro", "Leiria", "Coimbra", "Braga", "Santarem", "Faro", "Castelo Branco",
        "Setubal", "Evora", "Braganca", "Viseu", "Regiao Autonoma da Madeira", "Beja", "Viana do Castelo",
        "Vila Real", "Portalegre", "Guarda", "Regiao Autonoma dos Acores"
]

def generate_scotsmen_message() -> dict:
    
    # Generate a random number of Portuguese inhabitants converted 
    # into Scotsmen
    num_scotsmen_conversions = np.random.randint(200, 1_500)

    random_district = random.choice(all_districts)

    return {
        "district": random_district,
        "new_scotsmen": num_scotsmen_conversions,
        "timestamp": pendulum.now().to_datetime_string()
    }
    
def generate_bagpipe_message() -> dict:
    
    # Generate a random number of bagpipe sales
    num_bagpipe_sales = np.random.randint(50, 750)
    
    random_district = random.choice(all_districts)

    return {
        "district": random_district,
        "bagpipe_sales": num_bagpipe_sales,
        "timestamp": pendulum.now().to_datetime_string()
    }