__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

import pytest

from biosim.island.island import Island


def test_island_start():
    """
    Checks if the island can take in "Water" and can put them in a
    """
    Island('WW\nWW')


def test_if_start_with_1_1():
    """
    Tests that the first coordinate of the map is (1, 1)
    """
    testing = Island('WW\nWW')
    if list(testing.map.keys())[0] == (1, 1):
        assert True
    else:
        assert False


def test_same_len():
    """
    Checks if it raises ValueError when the rows does not have the same length
    """
    with pytest.raises(ValueError):
        Island("WWW\nWLLW\nWWW")
