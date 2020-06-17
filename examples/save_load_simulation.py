from biosim.simulation import BioSim
import numpy as np

np.random.seed(1)

ini_herbs = [
    {'loc': (5, 5), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 50} for _ in range(50)]}]


kart = """\
            WWWWWWWWWW
            WDDDDDDDDW
            WDDDDDDDDW
            WDDDHHDDDW
            WDDDLLDDDW
            WDDDHHDDDW
            WDDDLWDDDW
            WDDDWWHDDW
            WDDDDDDDDW
            WWWWWWWWWW"""

sim1 = BioSim(seed=123,
           ini_pop=ini_herbs,
           island_map=kart)
sim1.simulate(num_years=5)
sim1.save_simulation('state')

# Initiates BioSim with a state from a previous simulation
sim2 = BioSim(seed=123, ini_pop=[], island_map="WWW\nWWW\nWWW", save_name='state')
sim2.simulate(num_years=10)