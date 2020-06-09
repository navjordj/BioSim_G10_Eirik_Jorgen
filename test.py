from biosim.simulation import BioSim
import numpy as np

np.random.seed(0)
ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 20} for _ in range(50)]}]
            
ini_carn = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 6, 'weight': 20} for _ in range(20)]}]


kart = "WWW\nWLW\nWWW"


b = BioSim(seed=1, ini_pop=ini_herbs, island_map=kart)
b.add_population(ini_carn)

b.simulate(500)
