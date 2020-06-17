from biosim.simulation import BioSim
import numpy as np

np.random.seed(1)

ini_herbs = [
    {'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 50} for _ in range(50)]}]

kart = """\
            WWW
            WLW
            WWW"""


b = BioSim(seed=123,
           ini_pop=ini_herbs,
           island_map=kart,
           img_base='eirik/film',
           img_fmt='png',
           movie_format='mp4')

b.simulate(num_years=10, img_years=5)
b.make_movie()