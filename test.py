from biosim.simulation import BioSim
import numpy as np

# TODO: fix migration. The animals are now walking more then 1 cell a year

np.random.seed(1)

ini_herbs = [{'loc': (5, 5), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 20} for _ in range(50)]}]
            
ini_carn = [{'loc': (5, 5), 'pop': [{'species': 'Carnivore', 'age': 6, 'weight': 20} for _ in range(25)]}]


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
            WDDDLLDDDW
            WDDDHHDDDW
            WDDDWWDDDW
            WDDDHHDDDW
            WDDDLLDDDW
            WDDDDDDDDW
            WWWWWWWWWW"""

b = BioSim(seed=123, ini_pop=ini_herbs, island_map=kart)
b.add_population(ini_carn)

b.simulate(num_years=10)
b.save_simulation("10years")


