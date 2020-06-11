from biosim.simulation import BioSim
import numpy as np

import random

np.random.seed(1)
random.seed(1)
ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 10} for _ in range(20)]}]
            
ini_carn = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 6, 'weight': 10} for _ in range(0)]}]


kart = "WWW\nWLW\nWWW"


b = BioSim(seed=1, ini_pop=ini_herbs, island_map=kart)
b.add_population(ini_carn)

b.simulate(num_years=100)
