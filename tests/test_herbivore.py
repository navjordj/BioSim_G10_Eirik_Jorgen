__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.animals.herbivore import Herbivore

# @pytest.mark.skip(reason="Not implemented yet")
def test_init_herbivore():
    h = Herbivore(age=2, weight=10)
    assert h.weight == 10
    assert h.age == 2

    with pytest.raises(ValueError) as error:
        print(error)
        h = Herbivore(age=-1, weight=10)

    with pytest.raises(ValueError) as error:
        print(error)
        h = Herbivore(age=2, weight=-10)


def test_aging():
    a = Herbivore(age=4, weight=10)
    a.increase_age()
    assert a.age == 5