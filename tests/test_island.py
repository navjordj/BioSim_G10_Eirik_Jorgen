__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.island.island import Island


def test_island_start():
    '''
    Checks if the island can take in "Water" and can put them in a
    :return:
    '''
    l = Island('WW\nWW')
    print(f'\n{l.map}')

def test_same_len():
    '''
    Checks if it raises ValueError when the rows does not have the same length
    '''
    with pytest.raises(ValueError):
        Island("WWW\nWLLW\nWWW")