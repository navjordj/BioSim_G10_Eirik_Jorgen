from biosim.simulation import BioSim
import numpy as np

# TODO: fix migration. The animals are now walking more then 1 cell a year

np.random.seed(1)

ini_herbs = [{'loc': (5, 5), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 50} for _ in range(1000)]}]
            
ini_carn = [{'loc': (5, 5), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 50} for _ in range(1000)]}]


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

b = BioSim(seed=123, ini_pop=ini_herbs, island_map=kart)
b.add_population(ini_carn)

b.set_animal_parameters('Herbivore', {'mu': 1, 'omega': 0, 'gamma': 0, 'a_half': 1000, 'eta': 0})
b.set_animal_parameters('Carnivore', {'mu': 1, 'omega': 0, 'gamma': 0, 'F': 0, 'a_half': 1000, 'eta': 0})

b.simulate(num_years=50)
#b.simulate(num_years=10)
b.save_simulation("10years")


