__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.cell import Cell


def test_cell() -> None:
    Cell()


def test_change_params() -> None:
    k = Cell()
    with pytest.raises(ValueError):
        k.set_parameters(fodder=-1)
    k.set_parameters(fodder=300)
    assert k.fodder == 300


# TODO make sure fodder will go down
def test_eat_herbivore() -> None:
    k = Cell()
    food_fillup = 300
    k.fodder = food_fillup
    v = k.eat_herbivore
    pass
