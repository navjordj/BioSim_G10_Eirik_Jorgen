from biosim.simulation import BioSim
import numpy as np


# TODO: fix migration. The animals are now walking more then 1 cell a year

np.random.seed(1)

ini_herbs = [{'loc': (5, 5), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 50} for _ in range(50)]}]
            
ini_carn = [{'loc': (5, 5), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 50} for _ in range(50)]}]


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



b = BioSim(seed=123, ini_pop=ini_herbs, island_map=kart, img_base="img", movie_format="mp4")
b.add_population(ini_carn)

b.simulate(num_years=20)
b.make_movie()

