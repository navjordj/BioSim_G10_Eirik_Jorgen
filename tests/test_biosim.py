
__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest
import numpy as np
import scipy.stats as stats
from pytest_mock import mocker

from biosim.simulation import BioSim


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


def test_property_year() -> None:
    b = BioSim(island_map="WWWW\nWLHW\nWWWW",
               ini_pop=[],
               seed=1,
               save_name='ok')
    assert b.year() == 0


def test_save_name():
    b = BioSim(island_map="WWWW\nWLHW\nWWWW",
               ini_pop=[],
               seed=1,
               save_name='ok')
