__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.cell import Cell
from biosim.animals import Herbivore


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

@pytest.mark.skip("Not implemented yet")
def test_migration() -> None:
    pass

# TODO Check error of type Animal
def test_add_animal() -> None:
    c = Cell()
    a = Herbivore()
    c.add_animal(a)
    assert len(c.herbivores) == 1
    assert c.herbivores[0] == a