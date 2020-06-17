from biosim.simulation import BioSim
import numpy as np

np.random.seed(1)

ini_herbs = [
    {'loc': (5, 5), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 50} for _ in range(1000)]}]

ini_carn = [
    {'loc': (5, 5), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 50} for _ in range(1000)]}]

kart = """\
            WWWWWWWWWW
            WDDDDDDDDW
            WDDDDDDDDW
            WDDDDDDDDW
            WDDDDDDDDW
            WDDDDDDDDW
            WDDDDDDDDW
            WDDDDDDDDW
            WDDDDDDDDW
            WWWWWWWWWW"""


b = BioSim(seed=123,
           ini_pop=ini_herbs,
           island_map=kart)
b.set_animal_parameters('Herbivore', {'mu': 1, 'omega': 0, 'gamma': 0, 'a_half': 10000})

b.set_animal_parameters('Carnivore', {'mu': 1, 'omega': 0, 'gamma': 0, 'F': 0, 'a_half': 10000})
b.add_population(ini_carn)

b.simulate(num_years=10)
