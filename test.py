from biosim.simulation import BioSim
import numpy as np


np.random.seed(1)

ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': None} for _ in range(50)]}]
            
ini_carn = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 6, 'weight': None} for _ in range(30)]}]


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
            WWWWW
            WLLLW
            WLDLW
            WHHHW
            WWWWW"""

b = BioSim(seed=123, ini_pop=ini_herbs, island_map=kart)
b.add_population(ini_carn)

b.simulate(num_years=100)
