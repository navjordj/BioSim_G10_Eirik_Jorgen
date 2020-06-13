from biosim.simulation import BioSim
import numpy as np
import time

# TODO: fix migration. The animals are now walking more then 1 cell a year

np.random.seed(1)

ini_herbs = [{'loc': (5, 5), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 20} for _ in range(50)]}]
            
ini_carn = [{'loc': (5, 5), 'pop': [{'species': 'Carnivore', 'age': 6, 'weight': 20} for _ in range(20)]}]


kart = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHHHHLLLDDLLLHLLLWWW
               WHHLLLLLDDDLLLHHHHWWW
               WWHHHHLLLDDLLLHWWWWWW
               WHHHLLLLLDDLLLLLLLWWW
               WHHHHLLLLDDLLLLWWWWWW
               WWHHHHLLLLLLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""

# No vizualisation
# No prints to console

times = np.array([])
for _ in range(10):
    start_time = time.time()
    b = BioSim(seed=123, ini_pop=ini_herbs, island_map=kart)
    b.add_population(ini_carn)

    b.simulate(num_years=100) 
    end_time = time.time()
    times = np.append(times, end_time-start_time)

print(np.mean(times))
# MEAN: 29.938 seconds