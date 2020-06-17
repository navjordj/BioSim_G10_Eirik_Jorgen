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

b = BioSim(seed=123,
           ini_pop=ini_herbs,
           island_map=kart,
           img_base="img",
           movie_format="mp4")
b.simulate(num_years=5)

# TODO look at later
b.save_simulation('ok')
b.simulate(5)

c = BioSim(b.load_simlation('ok'), ini_pop=[])
c.simulate(num_years=10)