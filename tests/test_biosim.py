
__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'


import pytest
import numpy as np
import scipy.stats as stats
from pytest_mock import mocker

from biosim.simulation import BioSim

def plain_sim():
    """Return a simple island for used in various tests below"""
    return BioSim(island_map="WWWW\nWLHW\nWWWW",
                  ini_pop=[],
                  seed=1)

def test_init_biosim():
    b = BioSim(seed=1,
               ini_pop=[{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 50}]}],
               island_map='WWW\nWDW\nWWW')


def test_standard_specs() -> None:
    """
    Tests that all the default parameters is right
    """
    b = BioSim(island_map="WWWW\nWLHW\nWWWW",
           ini_pop=[],
           seed=1)

    assert b.ymax_animals == None
    assert b.cmax_animals == None
    assert b.hist_specs == {'weight': None, 'age': None, 'fitness': None}
    assert b.img_base == None
    assert b.img_fmt == "png"
    assert b.movie_format == None


@pytest.fixture
def test_serialization(plain_sim):
    plain_sim.simulate(num_years=5)

    island_pre_save = plain_sim.island_map
    plain_sim.save_simulation('test_save')

    plain_sim.load_simlation('test_save')
    island_post_save = plain_sim.island_map

    assert island_post_save == island_pre_save

    plain_sim.simulate(num_years=5)
    assert plain_sim.year == 10
