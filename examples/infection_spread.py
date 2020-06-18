from biosim.simulation import BioSim
import numpy as np

np.random.seed(1)

ini_herbs = [
    {'loc': (5, 5), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 50} for _ in range(50)]}]
ini_carn = [
    {'loc': (5, 5), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 50} for _ in range(50)]}]


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

sim = BioSim(seed=123,
           ini_pop=ini_herbs,
           island_map=kart)
sim.simulate(num_years=5)

sim.add_population(ini_carn)
sim.set_animal_parameters('Carnivore', {'infected': True})

sim.simulate(num_years=100)
